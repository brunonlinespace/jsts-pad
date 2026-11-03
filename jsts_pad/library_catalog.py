# JSTS Pad
# Copyright (C) 2026 Bruno Machado
# SPDX-License-Identifier: GPL-3.0-or-later
"""Language-aware insertion/reference Library for JavaScript-family source."""

from __future__ import annotations

from dataclasses import dataclass

CURSOR_MARKER = "[[cursor]]"
SELECTION_MARKER = "[[selection]]"
MAX_CUSTOM_SNIPPETS = 128
MAX_SNIPPET_NAME = 96
MAX_SNIPPET_DESCRIPTION = 320
MAX_SNIPPET_CHARACTERS = 50_000
LANGUAGES = frozenset({"javascript", "typescript", "jsx", "tsx"})


@dataclass(frozen=True, slots=True)
class LibrarySpec:
    key: str
    language: str
    label: str
    category: str
    opening: str
    closing: str
    description: str
    builtin: bool = True


def _s(key: str, language: str, label: str, category: str, opening: str, closing: str, description: str) -> LibrarySpec:
    return LibrarySpec(key, language, label, category, opening, closing, description, True)


COMMON_JS = (
    _s("js:const", "javascript", "const declaration", "Declarations", "const name = ", ";", "Declare a block-scoped constant."),
    _s("js:let", "javascript", "let declaration", "Declarations", "let name = ", ";", "Declare a block-scoped variable."),
    _s("js:function", "javascript", "function", "Functions", "function name() {\n    ", "\n}", "Create a named function."),
    _s("js:arrow", "javascript", "arrow function", "Functions", "const name = () => {\n    ", "\n};", "Create an arrow function."),
    _s("js:if", "javascript", "if block", "Control Flow", "if (condition) {\n    ", "\n}", "Create an if block."),
    _s("js:ifelse", "javascript", "if / else", "Control Flow", "if (condition) {\n    ", "\n} else {\n    \n}", "Create an if/else block."),
    _s("js:forof", "javascript", "for…of", "Control Flow", "for (const item of items) {\n    ", "\n}", "Iterate values from an iterable."),
    _s("js:foreach", "javascript", "forEach", "Arrays", "items.forEach((item) => {\n    ", "\n});", "Iterate an array with forEach."),
    _s("js:map", "javascript", ".map()", "Arrays", "const result = items.map((item) => ", ");", "Transform array values."),
    _s("js:filter", "javascript", ".filter()", "Arrays", "const result = items.filter((item) => ", ");", "Filter array values."),
    _s("js:object", "javascript", "object literal", "Objects", "const value = {\n    ", "\n};", "Create an object literal."),
    _s("js:destructure", "javascript", "object destructuring", "Objects", "const { name } = object;", "", "Destructure properties from an object."),
    _s("js:class", "javascript", "class", "Classes", "class Name {\n    constructor() {\n        ", "\n    }\n}", "Create a class with a constructor."),
    _s("js:import", "javascript", "import", "Modules", 'import { name } from "module";', "", "Import a named module export."),
    _s("js:export", "javascript", "export", "Modules", "export { name };", "", "Export a binding."),
    _s("js:async", "javascript", "async function", "Async", "async function name() {\n    ", "\n}", "Create an async function."),
    _s("js:await", "javascript", "await", "Async", "const result = await ", ";", "Await a promise."),
    _s("js:try", "javascript", "try / catch", "Errors", "try {\n    ", "\n} catch (error) {\n    \n}", "Handle an exception."),
    _s("js:query", "javascript", "querySelector", "Browser", 'const element = document.querySelector("selector");', "", "Select the first matching DOM element."),
    _s("js:event", "javascript", "addEventListener", "Browser", 'element.addEventListener("click", (event) => {\n    ', "\n});", "Attach a browser event listener."),
    _s("js:fetch", "javascript", "fetch", "Browser", 'const response = await fetch("url");', "", "Start an HTTP request in a browser/runtime that provides fetch."),
    _s("js:block-comment", "javascript", "block comment", "Comments", "/* ", " */", "Insert or wrap a block comment."),
)

TS_EXTRA = (
    _s("ts:type", "typescript", "type alias", "Types", "type Name = ", ";", "Declare a TypeScript type alias."),
    _s("ts:interface", "typescript", "interface", "Types", "interface Name {\n    ", "\n}", "Declare a TypeScript interface."),
    _s("ts:typed-const", "typescript", "typed const", "Types", "const name: Type = ", ";", "Declare a typed constant."),
    _s("ts:function", "typescript", "typed function", "Functions", "function name(value: Type): ReturnType {\n    ", "\n}", "Create a typed function."),
    _s("ts:generic", "typescript", "generic function", "Generics", "function identity<T>(value: T): T {\n    return ", ";\n}", "Create a generic identity-style function."),
    _s("ts:enum", "typescript", "enum", "Types", "enum Name {\n    ", "\n}", "Declare an enum."),
    _s("ts:class", "typescript", "typed class", "Classes", "class Name {\n    constructor(private value: Type) {}\n\n    ", "\n}", "Create a class with a typed constructor parameter."),
    _s("ts:as", "typescript", "type assertion", "Types", "value as Type", "", "Insert an `as` type assertion."),
)

JSX_EXTRA = (
    _s("jsx:element", "jsx", "element", "JSX", "<div>", "</div>", "Insert or wrap a JSX element."),
    _s("jsx:fragment", "jsx", "fragment", "JSX", "<>", "</>", "Insert or wrap a JSX fragment."),
    _s("jsx:expression", "jsx", "expression", "JSX", "{", "}", "Insert or wrap a JavaScript expression inside JSX."),
    _s("jsx:component", "jsx", "component", "Components", "function Component() {\n    return (\n        ", "\n    );\n}", "Create a simple JSX function component."),
    _s("jsx:prop", "jsx", "prop expression", "Props", "prop={", "}", "Insert a JSX prop expression."),
    _s("jsx:event", "jsx", "event prop", "Events", "onClick={() => {\n    ", "\n}}", "Insert an inline JSX event handler."),
    _s("jsx:conditional", "jsx", "conditional render", "Control Flow", "{condition && (\n    ", "\n)}", "Conditionally include JSX."),
    _s("jsx:list", "jsx", "list render", "Control Flow", "{items.map((item) => (\n    ", "\n))}", "Map a collection to JSX output."),
    _s("jsx:comment", "jsx", "JSX comment", "Comments", "{/* ", " */}", "Insert or wrap a comment in JSX markup."),
)

TSX_EXTRA = (
    _s("tsx:props", "tsx", "typed Props interface", "Types", "interface Props {\n    ", "\n}", "Declare props for a TSX component."),
    _s("tsx:component", "tsx", "typed component", "Components", "function Component({ value }: Props) {\n    return (\n        ", "\n    );\n}", "Create a TSX function component using a Props type."),
)

# Additive expansion of the original exp1 catalogue.  The original built-ins
# above are intentionally retained byte-for-byte; these tuples only add more
# frequently used JavaScript-family patterns.
JS_MORE = (
    _s("js:var", "javascript", "var declaration", "Declarations", "var name = ", ";", "Declare a function-scoped variable for legacy or compatibility-oriented code."),
    _s("js:array", "javascript", "array literal", "Declarations", "const items = [\n    ", "\n];", "Create an array literal."),
    _s("js:set", "javascript", "Set", "Declarations", "const values = new Set([", "]);", "Create a Set of unique values."),
    _s("js:map-collection", "javascript", "Map", "Declarations", "const lookup = new Map([\n    ", "\n]);", "Create a key/value Map collection."),
    _s("js:regexp", "javascript", "RegExp literal", "Declarations", "/pattern/", "g", "Insert a regular-expression literal."),
    _s("js:function-args", "javascript", "function with parameters", "Functions", "function name(value) {\n    ", "\n}", "Create a named function with a parameter."),
    _s("js:arrow-expression", "javascript", "arrow expression", "Functions", "const result = (value) => ", ";", "Create a concise arrow function expression."),
    _s("js:arrow-block", "javascript", "arrow function block", "Functions", "const name = (value) => {\n    ", "\n};", "Create an arrow function with a block body."),
    _s("js:default-parameter", "javascript", "default parameter", "Functions", "function name(value = defaultValue) {\n    ", "\n}", "Create a function using a default parameter value."),
    _s("js:rest-parameter", "javascript", "rest parameter", "Functions", "function name(...args) {\n    ", "\n}", "Collect remaining function arguments with a rest parameter."),
    _s("js:iife", "javascript", "IIFE", "Functions", "(() => {\n    ", "\n})();", "Create an immediately invoked function expression."),
    _s("js:generator", "javascript", "generator function", "Functions", "function* name() {\n    yield ", ";\n}", "Create a generator function."),
    _s("js:ternary", "javascript", "ternary expression", "Control Flow", "const result = condition ? ", " : fallback;", "Create a conditional expression."),
    _s("js:switch", "javascript", "switch", "Control Flow", "switch (value) {\n    case expected:\n        ", "\n        break;\n    default:\n        break;\n}", "Create a switch statement with a default branch."),
    _s("js:for", "javascript", "for loop", "Control Flow", "for (let i = 0; i < items.length; i += 1) {\n    ", "\n}", "Create an indexed for loop."),
    _s("js:forin", "javascript", "for…in", "Control Flow", "for (const key in object) {\n    ", "\n}", "Iterate enumerable object property names."),
    _s("js:while", "javascript", "while loop", "Control Flow", "while (condition) {\n    ", "\n}", "Create a while loop."),
    _s("js:dowhile", "javascript", "do…while", "Control Flow", "do {\n    ", "\n} while (condition);", "Create a do/while loop."),
    _s("js:find", "javascript", ".find()", "Arrays", "const item = items.find((item) => ", ");", "Find the first array item matching a predicate."),
    _s("js:find-index", "javascript", ".findIndex()", "Arrays", "const index = items.findIndex((item) => ", ");", "Find the index of the first matching array item."),
    _s("js:some", "javascript", ".some()", "Arrays", "const hasMatch = items.some((item) => ", ");", "Test whether at least one array item matches."),
    _s("js:every", "javascript", ".every()", "Arrays", "const allMatch = items.every((item) => ", ");", "Test whether every array item matches."),
    _s("js:reduce", "javascript", ".reduce()", "Arrays", "const result = items.reduce((accumulator, item) => {\n    ", "\n    return accumulator;\n}, initialValue);", "Reduce an array to a single accumulated value."),
    _s("js:flatmap", "javascript", ".flatMap()", "Arrays", "const result = items.flatMap((item) => ", ");", "Map array items and flatten one level."),
    _s("js:includes", "javascript", ".includes()", "Arrays", "const contains = items.includes(", ");", "Test whether an array contains a value."),
    _s("js:sort-number", "javascript", "numeric sort", "Arrays", "items.sort((a, b) => ", ");", "Sort numeric-style values with an explicit comparator."),
    _s("js:array-destructure", "javascript", "array destructuring", "Arrays", "const [first, second] = ", ";", "Destructure values from an iterable or array."),
    _s("js:array-spread", "javascript", "array spread copy", "Arrays", "const copy = [...", "];", "Create a shallow array copy with spread syntax."),
    _s("js:object-spread", "javascript", "object spread copy", "Objects", "const copy = { ...", " };", "Create a shallow object copy with spread syntax."),
    _s("js:object-merge", "javascript", "object spread merge", "Objects", "const merged = { ...first, ...", " };", "Merge object properties with spread syntax."),
    _s("js:object-keys", "javascript", "Object.keys()", "Objects", "const keys = Object.keys(", ");", "Get an object's own enumerable property names."),
    _s("js:object-values", "javascript", "Object.values()", "Objects", "const values = Object.values(", ");", "Get an object's own enumerable property values."),
    _s("js:object-entries", "javascript", "Object.entries()", "Objects", "for (const [key, value] of Object.entries(object)) {\n    ", "\n}", "Iterate an object's own enumerable key/value pairs."),
    _s("js:optional-chaining", "javascript", "optional chaining", "Objects", "const value = object?.", ";", "Safely access a property through optional chaining."),
    _s("js:nullish", "javascript", "nullish coalescing", "Objects", "const value = possibleValue ?? ", ";", "Provide a fallback only for null or undefined."),
    _s("js:template-literal", "javascript", "template literal", "Strings", "`", "`", "Insert or wrap a JavaScript template literal."),
    _s("js:string-includes", "javascript", "string includes", "Strings", "const contains = text.includes(", ");", "Test whether a string contains a value."),
    _s("js:split-join", "javascript", "split / join", "Strings", "const result = text.split(delimiter).join(", ");", "Split a string and join the pieces again."),
    _s("js:async-arrow", "javascript", "async arrow function", "Async", "const name = async () => {\n    ", "\n};", "Create an asynchronous arrow function."),
    _s("js:promise", "javascript", "Promise", "Async", "const promise = new Promise((resolve, reject) => {\n    ", "\n});", "Create a Promise with resolve and reject callbacks."),
    _s("js:promise-all", "javascript", "Promise.all()", "Async", "const results = await Promise.all([\n    ", "\n]);", "Await several promises and fail if one rejects."),
    _s("js:promise-allsettled", "javascript", "Promise.allSettled()", "Async", "const results = await Promise.allSettled([\n    ", "\n]);", "Await several promises and retain every outcome."),
    _s("js:fetch-json", "javascript", "fetch JSON", "Async", "const response = await fetch(url);\nif (!response.ok) throw new Error(`HTTP ${response.status}`);\nconst data = await response.json();\n", "", "Fetch a resource, check the response and parse JSON."),
    _s("js:fetch-post-json", "javascript", "fetch POST JSON", "Async", "const response = await fetch(url, {\n    method: \"POST\",\n    headers: { \"Content-Type\": \"application/json\" },\n    body: JSON.stringify(", "),\n});", "POST JSON using fetch."),
    _s("js:try-finally", "javascript", "try / catch / finally", "Errors", "try {\n    ", "\n} catch (error) {\n    \n} finally {\n    \n}", "Handle an exception and run cleanup code."),
    _s("js:throw", "javascript", "throw Error", "Errors", "throw new Error(", ");", "Throw a standard Error."),
    _s("js:import-default", "javascript", "default import", "Modules", "import name from \"module\";", "", "Import a module's default export."),
    _s("js:import-namespace", "javascript", "namespace import", "Modules", "import * as name from \"module\";", "", "Import all module exports into a namespace object."),
    _s("js:export-default", "javascript", "default export", "Modules", "export default ", ";", "Export a default value or declaration."),
    _s("js:dynamic-import", "javascript", "dynamic import", "Modules", "const module = await import(", ");", "Load an ES module dynamically."),
    _s("js:query-all", "javascript", "querySelectorAll", "Browser", "const elements = document.querySelectorAll(\"selector\");", "", "Select all DOM elements matching a CSS selector."),
    _s("js:create-element", "javascript", "createElement", "Browser", "const element = document.createElement(\"", "\");", "Create a DOM element."),
    _s("js:append", "javascript", "append element", "Browser", "parent.append(", ");", "Append content to a DOM node."),
    _s("js:class-toggle", "javascript", "classList.toggle", "Browser", "element.classList.toggle(\"", "\");", "Toggle a CSS class on a DOM element."),
    _s("js:dom-ready", "javascript", "DOMContentLoaded", "Browser", "document.addEventListener(\"DOMContentLoaded\", () => {\n    ", "\n});", "Run code after the initial DOM has been parsed."),
    _s("js:form-submit", "javascript", "form submit handler", "Browser", "form.addEventListener(\"submit\", (event) => {\n    event.preventDefault();\n    ", "\n});", "Handle a browser form submission without its default navigation."),
    _s("js:local-storage-get", "javascript", "localStorage get", "Browser", "const value = localStorage.getItem(\"", "\");", "Read a browser localStorage value."),
    _s("js:local-storage-set", "javascript", "localStorage set", "Browser", "localStorage.setItem(\"key\", ", ");", "Write a browser localStorage value."),
    _s("js:set-timeout", "javascript", "setTimeout", "Timers", "const timeoutId = setTimeout(() => {\n    ", "\n}, 1000);", "Run code once after a delay."),
    _s("js:set-interval", "javascript", "setInterval", "Timers", "const intervalId = setInterval(() => {\n    ", "\n}, 1000);", "Run code repeatedly on an interval."),
    _s("js:json-parse", "javascript", "JSON.parse()", "JSON", "const value = JSON.parse(", ");", "Parse a JSON string."),
    _s("js:json-stringify", "javascript", "JSON.stringify()", "JSON", "const json = JSON.stringify(", ", null, 2);", "Serialize a value to formatted JSON text."),
    _s("js:console-log", "javascript", "console.log", "Console", "console.log(", ");", "Write a diagnostic value to the console."),
    _s("js:console-warn", "javascript", "console.warn", "Console", "console.warn(", ");", "Write a warning to the console."),
    _s("js:console-error", "javascript", "console.error", "Console", "console.error(", ");", "Write an error to the console."),
    _s("js:console-table", "javascript", "console.table", "Console", "console.table(", ");", "Display tabular data in supporting developer consoles."),
    _s("js:url", "javascript", "URL", "Web APIs", "const parsedUrl = new URL(", ");", "Parse or construct a URL."),
    _s("js:url-search-params", "javascript", "URLSearchParams", "Web APIs", "const params = new URLSearchParams(", ");", "Read or construct URL query parameters."),
    _s("js:date", "javascript", "Date", "Utilities", "const now = new Date(", ");", "Create a Date value."),
    _s("js:random-int", "javascript", "random integer", "Utilities", "const value = Math.floor(Math.random() * ", ");", "Generate an integer from zero up to an exclusive maximum."),
    _s("js:node-args", "javascript", "process.argv", "Node.js", "const args = process.argv.slice(", ");", "Read command-line arguments in Node.js."),
    _s("js:node-env", "javascript", "process.env", "Node.js", "const value = process.env.", ";", "Read an environment variable in Node.js."),
    _s("js:node-read-file", "javascript", "read file (fs/promises)", "Node.js", "import { readFile } from \"node:fs/promises\";\n\nconst text = await readFile(path, \"utf8\");\n", "", "Read a UTF-8 file with Node.js promises APIs."),
    _s("js:node-write-file", "javascript", "write file (fs/promises)", "Node.js", "import { writeFile } from \"node:fs/promises\";\n\nawait writeFile(path, ", ", \"utf8\");", "Write a UTF-8 file with Node.js promises APIs."),
    _s("js:node-path-join", "javascript", "path.join", "Node.js", "import { join } from \"node:path\";\n\nconst path = join(", ");", "Join path segments with Node.js."),
)

TS_MORE = (
    _s("ts:union", "typescript", "union type", "Types", "type Name = First | ", ";", "Declare a union type."),
    _s("ts:intersection", "typescript", "intersection type", "Types", "type Name = First & ", ";", "Declare an intersection type."),
    _s("ts:tuple", "typescript", "tuple type", "Types", "const pair: [string, number] = [", "];", "Declare and initialize a typed tuple."),
    _s("ts:readonly-array", "typescript", "readonly array", "Types", "const items: readonly Type[] = [\n    ", "\n];", "Declare an array that cannot be mutated through this reference."),
    _s("ts:nullable", "typescript", "nullable type", "Types", "let value: Type | null = ", ";", "Declare a value that may be null."),
    _s("ts:literal-union", "typescript", "literal union", "Types", "type Status = \"idle\" | \"loading\" | ", ";", "Declare a union of literal values."),
    _s("ts:record", "typescript", "Record", "Utility Types", "type Lookup = Record<string, ", ">;", "Create a key/value object type with Record."),
    _s("ts:partial", "typescript", "Partial", "Utility Types", "type Update = Partial<", ">;", "Make every property of a type optional."),
    _s("ts:required", "typescript", "Required", "Utility Types", "type Complete = Required<", ">;", "Make every property of a type required."),
    _s("ts:pick", "typescript", "Pick", "Utility Types", "type Selected = Pick<Type, ", ">;", "Select a subset of properties from a type."),
    _s("ts:omit", "typescript", "Omit", "Utility Types", "type Remaining = Omit<Type, ", ">;", "Remove selected properties from a type."),
    _s("ts:return-type", "typescript", "ReturnType", "Utility Types", "type Result = ReturnType<typeof ", ">;", "Extract a function's return type."),
    _s("ts:parameters", "typescript", "Parameters", "Utility Types", "type Args = Parameters<typeof ", ">;", "Extract a function's parameter tuple."),
    _s("ts:keyof", "typescript", "keyof", "Type Operators", "type Keys = keyof ", ";", "Create a union of known property names."),
    _s("ts:typeof", "typescript", "typeof type", "Type Operators", "type ValueType = typeof ", ";", "Derive a type from a value declaration."),
    _s("ts:indexed-access", "typescript", "indexed access type", "Type Operators", "type Property = Type[", "];", "Extract a property type through indexed access."),
    _s("ts:as-const", "typescript", "as const", "Type Operators", "const value = ", " as const;", "Preserve literal values and readonly structure with a const assertion."),
    _s("ts:satisfies", "typescript", "satisfies", "Type Operators", "const value = ", " satisfies Type;", "Check that a value satisfies a type without replacing its inferred type."),
    _s("ts:non-null", "typescript", "non-null assertion", "Type Operators", "const value = possibleValue!", ";", "Assert that a value is not null or undefined."),
    _s("ts:optional-property", "typescript", "optional property", "Interfaces", "interface Name {\n    value?: ", ";\n}", "Declare an optional interface property."),
    _s("ts:readonly-property", "typescript", "readonly property", "Interfaces", "interface Name {\n    readonly value: ", ";\n}", "Declare a readonly interface property."),
    _s("ts:index-signature", "typescript", "index signature", "Interfaces", "interface Lookup {\n    [key: string]: ", ";\n}", "Declare an object with string-indexed values."),
    _s("ts:generic-interface", "typescript", "generic interface", "Generics", "interface Result<T> {\n    value: ", ";\n}", "Declare an interface parameterized by a generic type."),
    _s("ts:generic-type", "typescript", "generic type alias", "Generics", "type Result<T> = {\n    value: ", ";\n};", "Declare a generic object type alias."),
    _s("ts:generic-constraint", "typescript", "generic constraint", "Generics", "function name<T extends Base>(value: T): T {\n    return ", ";\n}", "Constrain a generic type parameter."),
    _s("ts:typed-arrow", "typescript", "typed arrow function", "Functions", "const name = (value: Type): ReturnType => ", ";", "Create a typed arrow function."),
    _s("ts:async-function", "typescript", "typed async function", "Functions", "async function name(): Promise<Type> {\n    return ", ";\n}", "Create an async function with an explicit Promise return type."),
    _s("ts:callback-type", "typescript", "callback type", "Functions", "type Callback = (value: Type) => ", ";", "Declare a reusable function/callback type."),
    _s("ts:overload", "typescript", "function overload", "Functions", "function name(value: string): string;\nfunction name(value: number): number;\nfunction name(value: string | number): string | number {\n    ", "\n}", "Declare overload signatures plus one implementation."),
    _s("ts:type-guard", "typescript", "type guard", "Narrowing", "function isType(value: unknown): value is Type {\n    return ", ";\n}", "Create a user-defined type predicate."),
    _s("ts:assertion-function", "typescript", "assertion function", "Narrowing", "function assertType(value: unknown): asserts value is Type {\n    if (!condition) {\n        throw new Error(\"Invalid value\");\n    }\n    ", "\n}", "Create an assertion function that narrows a value."),
    _s("ts:unknown-guard", "typescript", "unknown guard", "Narrowing", "if (typeof value === \"", "\") {\n    \n}", "Narrow an unknown value with typeof."),
    _s("ts:discriminated-union", "typescript", "discriminated union", "Narrowing", "type Result =\n    | { kind: \"success\"; value: Type }\n    | { kind: \"error\"; error: Error }\n    | { kind: ", " };", "Declare a discriminated union for exhaustive narrowing."),
    _s("ts:exhaustive-never", "typescript", "exhaustive never check", "Narrowing", "const exhaustive: never = ", ";\nthrow new Error(`Unhandled value: ${exhaustive}`);", "Assert exhaustiveness after narrowing a union."),
    _s("ts:import-type", "typescript", "type-only import", "Modules", "import type { Type } from \"", "\";", "Import a TypeScript type without a runtime import."),
    _s("ts:export-type", "typescript", "type-only export", "Modules", "export type { Type } from \"", "\";", "Re-export a type without creating a runtime binding."),
    _s("ts:implements", "typescript", "class implements", "Classes", "class Name implements Interface {\n    ", "\n}", "Create a class implementing an interface."),
    _s("ts:abstract-class", "typescript", "abstract class", "Classes", "abstract class Base {\n    abstract method(): ", ";\n}", "Declare an abstract base class and abstract method."),
    _s("ts:parameter-property", "typescript", "constructor parameter property", "Classes", "class Name {\n    constructor(public readonly value: ", ") {}\n}", "Declare and initialize a class property through the constructor parameter."),
    _s("ts:declare", "typescript", "declare const", "Declarations", "declare const name: ", ";", "Describe a value supplied by another runtime or script."),
)

JSX_MORE = (
    _s("jsx:self-closing", "jsx", "self-closing element", "JSX", "<Component ", " />", "Insert a self-closing JSX element or component."),
    _s("jsx:div-class", "jsx", "div with className", "JSX", "<div className=\"class-name\">", "</div>", "Insert or wrap a div with a className."),
    _s("jsx:inline-style", "jsx", "inline style", "JSX", "style={{ ", " }}", "Insert an inline JSX style object."),
    _s("jsx:aria-label", "jsx", "aria-label", "Accessibility", "aria-label=\"", "\"", "Insert an accessible name attribute."),
    _s("jsx:label-input", "jsx", "label + input", "Accessibility", "<label htmlFor=\"field\">Label</label>\n<input id=\"field\" name=\"field\" ", " />", "Insert an associated label and input control."),
    _s("jsx:button", "jsx", "button", "Elements", "<button type=\"button\" onClick={handleClick}>\n    ", "\n</button>", "Insert a button wired to a click handler."),
    _s("jsx:link", "jsx", "anchor", "Elements", "<a href=\"", "\">Link</a>", "Insert a standard anchor element."),
    _s("jsx:image", "jsx", "image", "Elements", "<img src={src} alt=\"", "\" />", "Insert an image with alt text."),
    _s("jsx:arrow-component", "jsx", "arrow component", "Components", "const Component = () => {\n    return (\n        ", "\n    );\n};", "Create a JSX arrow-function component."),
    _s("jsx:component-props", "jsx", "component with props", "Components", "function Component({ value }) {\n    return (\n        ", "\n    );\n}", "Create a component that destructures a prop."),
    _s("jsx:children", "jsx", "children prop", "Props", "function Component({ children }) {\n    return (\n        ", "\n    );\n}", "Create a component that renders children."),
    _s("jsx:spread-props", "jsx", "spread props", "Props", "<Component {...", "} />", "Spread an object of props onto a component."),
    _s("jsx:boolean-prop", "jsx", "boolean prop", "Props", "<Component ", " />", "Insert a component ready for a boolean shorthand prop."),
    _s("jsx:ternary", "jsx", "ternary render", "Control Flow", "{condition ? (\n    ", "\n) : (\n    fallback\n)}", "Render one of two JSX branches."),
    _s("jsx:list-key", "jsx", "list render with key", "Control Flow", "{items.map((item) => (\n    <div key={item.id}>\n        ", "\n    </div>\n))}", "Render a list with stable JSX keys."),
    _s("jsx:render-null", "jsx", "early return null", "Control Flow", "if (!condition) {\n    return null;\n}\n\n", "", "Return no JSX when a condition is not met."),
    _s("jsx:onchange", "jsx", "onChange handler", "Events", "onChange={(event) => {\n    ", "\n}}", "Insert an inline JSX change handler."),
    _s("jsx:onsubmit", "jsx", "onSubmit handler", "Events", "onSubmit={(event) => {\n    event.preventDefault();\n    ", "\n}}", "Insert an inline JSX form submit handler."),
    _s("jsx:onkeydown", "jsx", "onKeyDown handler", "Events", "onKeyDown={(event) => {\n    ", "\n}}", "Insert an inline keyboard handler."),
    _s("jsx:controlled-input", "jsx", "controlled input", "Forms", "<input\n    value={value}\n    onChange={(event) => setValue(event.target.value)}\n    ", "\n/>", "Insert a controlled text input."),
    _s("jsx:checkbox", "jsx", "controlled checkbox", "Forms", "<input\n    type=\"checkbox\"\n    checked={checked}\n    onChange={(event) => setChecked(event.target.checked)}\n    ", "\n/>", "Insert a controlled checkbox."),
    _s("jsx:select", "jsx", "controlled select", "Forms", "<select value={value} onChange={(event) => setValue(event.target.value)}>\n    ", "\n</select>", "Insert a controlled select element."),
    _s("jsx:textarea", "jsx", "controlled textarea", "Forms", "<textarea\n    value={value}\n    onChange={(event) => setValue(event.target.value)}\n>", "</textarea>", "Insert a controlled textarea."),
    _s("jsx:form", "jsx", "form", "Forms", "<form onSubmit={handleSubmit}>\n    ", "\n</form>", "Insert a form wired to a submit handler."),
    _s("jsx:use-state", "jsx", "useState", "React Hooks", "const [value, setValue] = useState(", ");", "Create a React state value and setter."),
    _s("jsx:use-effect", "jsx", "useEffect", "React Hooks", "useEffect(() => {\n    ", "\n}, []);", "Create a React effect that runs after mounting."),
    _s("jsx:use-effect-cleanup", "jsx", "useEffect with cleanup", "React Hooks", "useEffect(() => {\n    ", "\n\n    return () => {\n        \n    };\n}, []);", "Create a React effect with cleanup."),
    _s("jsx:use-memo", "jsx", "useMemo", "React Hooks", "const value = useMemo(() => ", ", [dependency]);", "Memoize a computed value in React."),
    _s("jsx:use-callback", "jsx", "useCallback", "React Hooks", "const handleAction = useCallback(() => {\n    ", "\n}, [dependency]);", "Memoize a callback in React."),
    _s("jsx:use-ref", "jsx", "useRef", "React Hooks", "const ref = useRef(", ");", "Create a mutable React ref."),
    _s("jsx:use-context", "jsx", "useContext", "React Hooks", "const value = useContext(", ");", "Read a React context value."),
    _s("jsx:use-reducer", "jsx", "useReducer", "React Hooks", "const [state, dispatch] = useReducer(reducer, ", ");", "Create reducer-managed React state."),
    _s("jsx:hooks-import", "jsx", "React hooks import", "Modules", "import { useEffect, useState } from \"react\";", "", "Import frequently used React hooks."),
)

TSX_MORE = (
    _s("tsx:type-props", "tsx", "typed Props alias", "Types", "type Props = {\n    ", "\n};", "Declare component props with a type alias."),
    _s("tsx:children", "tsx", "typed children props", "Types", "type Props = {\n    children: React.ReactNode;\n    ", "\n};", "Declare props containing renderable React children."),
    _s("tsx:props-with-children", "tsx", "PropsWithChildren", "Types", "type Props = React.PropsWithChildren<{\n    ", "\n}>;", "Add React children to a props object type."),
    _s("tsx:intrinsic-props", "tsx", "intrinsic element props", "Types", "type Props = React.ComponentProps<\"", "\">;", "Reuse the props type of an intrinsic JSX element."),
    _s("tsx:css-properties", "tsx", "CSSProperties", "Types", "const style: React.CSSProperties = {\n    ", "\n};", "Create a typed inline style object."),
    _s("tsx:arrow-component", "tsx", "typed arrow component", "Components", "const Component = ({ value }: Props) => {\n    return (\n        ", "\n    );\n};", "Create a typed TSX arrow-function component."),
    _s("tsx:generic-component", "tsx", "generic component", "Components", "function Component<T>({ items }: { items: T[] }) {\n    return (\n        ", "\n    );\n}", "Create a generic TSX component."),
    _s("tsx:discriminated-props", "tsx", "discriminated component props", "Components", "type Props =\n    | { kind: \"text\"; value: string }\n    | { kind: \"number\"; value: number }\n    | { kind: ", " };", "Declare mutually distinguishable TSX component props."),
    _s("tsx:use-state", "tsx", "typed useState", "React Hooks", "const [value, setValue] = useState<Type>(", ");", "Create typed React state."),
    _s("tsx:nullable-state", "tsx", "nullable useState", "React Hooks", "const [value, setValue] = useState<Type | null>(", ");", "Create React state that may be null."),
    _s("tsx:use-ref", "tsx", "typed DOM useRef", "React Hooks", "const ref = useRef<HTMLDivElement | null>(", ");", "Create a ref to a DOM element."),
    _s("tsx:typed-context", "tsx", "typed context", "React Hooks", "const Context = createContext<Type | undefined>(undefined);\n", "", "Create a typed React context that requires a provider."),
    _s("tsx:typed-reducer", "tsx", "typed reducer", "React Hooks", "type State = { value: number };\ntype Action = { type: \"increment\" } | { type: \"reset\" };\n\nfunction reducer(state: State, action: Action): State {\n    ", "\n}", "Create typed reducer state and actions."),
    _s("tsx:mouse-event", "tsx", "typed mouse event", "Events", "function handleClick(event: React.MouseEvent<HTMLButtonElement>) {\n    ", "\n}", "Create a typed button mouse-event handler."),
    _s("tsx:change-event", "tsx", "typed input change event", "Events", "function handleChange(event: React.ChangeEvent<HTMLInputElement>) {\n    ", "\n}", "Create a typed input change-event handler."),
    _s("tsx:form-event", "tsx", "typed form event", "Events", "function handleSubmit(event: React.FormEvent<HTMLFormElement>) {\n    event.preventDefault();\n    ", "\n}", "Create a typed form submit handler."),
    _s("tsx:keyboard-event", "tsx", "typed keyboard event", "Events", "function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {\n    ", "\n}", "Create a typed keyboard-event handler."),
    _s("tsx:custom-hook", "tsx", "typed custom hook", "React Hooks", "function useValue(initialValue: Type): Type {\n    ", "\n}", "Create a typed custom React hook."),
    _s("tsx:forward-ref", "tsx", "forwardRef component", "Components", "const Component = React.forwardRef<HTMLDivElement, Props>(({ value }, ref) => {\n    return (\n        ", "\n    );\n});", "Create a typed component that forwards a DOM ref."),
    _s("tsx:html-props", "tsx", "extend HTML attributes", "Types", "interface Props extends React.HTMLAttributes<HTMLDivElement> {\n    ", "\n}", "Extend the standard attributes for a div element."),
    _s("tsx:button-props", "tsx", "extend button attributes", "Types", "interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {\n    ", "\n}", "Extend standard button attributes with custom props."),
    _s("tsx:typed-map", "tsx", "typed list render", "Control Flow", "{items.map((item: Type) => (\n    <Component key={item.id} value={", "} />\n))}", "Render a typed list of TSX components."),
    _s("tsx:async-submit", "tsx", "typed async submit", "Events", "async function handleSubmit(event: React.FormEvent<HTMLFormElement>): Promise<void> {\n    event.preventDefault();\n    ", "\n}", "Create an asynchronous typed form submit handler."),
    _s("tsx:react-type-import", "tsx", "React type import", "Modules", "import type { ReactNode } from \"react\";", "", "Import a React type without adding a runtime binding."),
)


def _clone_for_language(spec: LibrarySpec, language: str) -> LibrarySpec:
    return LibrarySpec(
        f"{language}:{spec.key}",
        language,
        spec.label,
        spec.category,
        spec.opening,
        spec.closing,
        spec.description,
        True,
    )


def builtins_for_language(language: str) -> tuple[LibrarySpec, ...]:
    javascript_specs = COMMON_JS + JS_MORE
    typescript_specs = TS_EXTRA + TS_MORE
    jsx_specs = JSX_EXTRA + JSX_MORE
    if language == "javascript":
        return javascript_specs
    if language == "typescript":
        return tuple(_clone_for_language(s, "typescript") for s in javascript_specs) + typescript_specs
    if language == "jsx":
        return tuple(_clone_for_language(s, "jsx") for s in javascript_specs) + jsx_specs
    if language == "tsx":
        return (
            tuple(_clone_for_language(s, "tsx") for s in javascript_specs)
            + tuple(_clone_for_language(s, "tsx") for s in typescript_specs)
            + tuple(_clone_for_language(s, "tsx") for s in jsx_specs)
            + TSX_EXTRA
            + TSX_MORE
        )
    return ()


def normalise_custom_snippets(raw: object) -> list[LibrarySpec]:
    if not isinstance(raw, list):
        return []
    result: list[LibrarySpec] = []
    seen: set[str] = set()
    for item in raw[:MAX_CUSTOM_SNIPPETS]:
        if not isinstance(item, dict):
            continue
        key = item.get("id")
        language = item.get("language")
        label = item.get("name")
        category = item.get("category", "Custom")
        content = item.get("content")
        description = item.get("description", "Custom snippet")
        if (
            not isinstance(key, str)
            or not key.startswith("user:")
            or len(key) > 180
            or key in seen
            or language not in LANGUAGES
            or not isinstance(label, str)
            or not label.strip()
            or len(label) > MAX_SNIPPET_NAME
            or not isinstance(category, str)
            or not category.strip()
            or len(category) > 64
            or not isinstance(content, str)
            or len(content) > MAX_SNIPPET_CHARACTERS
            or not isinstance(description, str)
            or len(description) > MAX_SNIPPET_DESCRIPTION
        ):
            continue
        seen.add(key)
        if CURSOR_MARKER in content:
            opening, closing = content.split(CURSOR_MARKER, 1)
        else:
            opening, closing = content, ""
        result.append(
            LibrarySpec(
                key,
                str(language),
                label.strip(),
                category.strip(),
                opening,
                closing,
                description.strip() or "Custom snippet",
                False,
            )
        )
    return result


def serialise_custom_snippets(snippets: list[LibrarySpec]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for spec in snippets:
        if spec.builtin:
            continue
        content = spec.opening + (CURSOR_MARKER + spec.closing if spec.closing else "")
        result.append(
            {
                "id": spec.key,
                "language": spec.language,
                "name": spec.label,
                "category": spec.category,
                "content": content,
                "description": spec.description,
            }
        )
    return result
