#!/usr/bin/env python3
from __future__ import annotations
import hashlib, re, struct, unittest, xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PKG=ROOT/'jsts_pad'

class PackagingTests(unittest.TestCase):
    def test_portable_outer_tree(self):
        self.assertEqual({p.name for p in ROOT.iterdir()}, {'README.md','main.py','suite-pythoine-component.json','jsts_pad'})
    def test_root_public_readme_contract(self):
        readme=ROOT/'README.md'
        self.assertTrue(readme.is_file())
        text=readme.read_text(encoding='utf-8')
        self.assertIn('Current release: **0.1.3**', text)
        builder=(PKG/'packaging/fedora/build-appimage.sh').read_text(encoding='utf-8')
        self.assertIn('PUBLIC_README="${PROJECT_ROOT}/README.md"', builder)
        self.assertIn('Root README SHA-256:', builder)

    def test_suite_component_manifest(self):
        import json
        data=json.loads((ROOT/'suite-pythoine-component.json').read_text())
        self.assertEqual(data['id'],'jsts-pad')
        self.assertEqual(data['version'],'0.1.3')
        self.assertEqual(data['component_kind'],'editor')
        self.assertEqual(data['extensions'],['.js','.mjs','.cjs','.ts','.mts','.cts','.jsx','.tsx'])
        self.assertEqual(data['portable_command'],['main.py'])
        self.assertEqual(data['tagline'],'Friendly. Fast. Focused.')
    def test_identity_metadata(self):
        desktop=(PKG/'packaging/appimage/jsts-pad.desktop').read_text()
        self.assertIn('Name=JSTS Pad',desktop); self.assertIn('Exec=jsts-pad %F',desktop); self.assertIn('Icon=jsts-pad',desktop)
        self.assertIn('application/javascript',desktop); self.assertIn('text/typescript',desktop)
        self.assertNotIn('text/html',desktop); self.assertNotIn('application/xml',desktop)
        tree=ET.parse(PKG/'packaging/appimage/io.github.brunonlinespace.jsts-pad.metainfo.xml')
        self.assertEqual(tree.getroot().findtext('id'),'io.github.brunonlinespace.jsts-pad')
    def test_official_logo_exact_hash_and_rgba(self):
        p=PKG/'assets/icons/jsts-pad-master.png'; data=p.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),'61b6574b4c9da7c92e01e309aa0d0fb795c0010e57f84b56f332743ab06a5e6e')
        self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
        width,height,bit_depth,color_type=struct.unpack('>IIBB',data[16:26])
        self.assertEqual((width,height,bit_depth,color_type),(1024,1024,8,6))
    def test_icon_family_exists(self):
        for size in (16,24,32,48,64,128,256,512): self.assertTrue((PKG/f'assets/icons/jsts-pad-{size}.png').is_file())
    def test_pyinstaller_excludes_unused_heavy_qt(self):
        spec=(PKG/'packaging/pyinstaller/jsts-pad.spec').read_text()
        for module in ('PyQt6.QtPdf','PyQt6.QtPdfWidgets','PyQt6.QtPrintSupport','PyQt6.QtWebEngineCore','PyQt6.QtWebEngineWidgets'):
            self.assertIn(module,spec)
    def test_builder_outputs_jsts_name(self):
        script=(PKG/'packaging/fedora/build-appimage.sh').read_text()
        self.assertIn('JSTS-Pad-${APP_VERSION}-${ARCH}.AppImage',script)
        self.assertNotIn('Timblee-Pad-',script)
    def test_no_privileged_install_invocations(self):
        for path in (PKG/'packaging/fedora').glob('*.sh'):
            for line in path.read_text().splitlines():
                stripped=line.strip()
                if not stripped or stripped.startswith('#'): continue
                self.assertIsNone(re.match(r'^(?:sudo|dnf|pkexec|su)(?:\s|$)',stripped), f'{path.name}: {stripped}')
    def test_host_dep_helper_only_checks(self):
        helper=(PKG/'packaging/fedora/install-build-deps.sh').read_text()
        self.assertIn('host prerequisite check',helper); self.assertNotIn(' install -y ',helper)
    def test_no_execution_stack_in_runtime_requirements(self):
        req=(PKG/'requirements.txt').read_text().lower()
        for token in ('node','npm','typescript','eslint','prettier','webengine'): self.assertNotIn(token,req)
    def test_appimage_apprun_identity(self):
        apprun=(PKG/'packaging/appimage/AppRun').read_text()
        self.assertIn('jsts-pad',apprun); self.assertNotIn('timblee',apprun.lower())

if __name__ == "__main__": unittest.main()
