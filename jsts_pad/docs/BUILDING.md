# Building JSTS Pad

## Portable source

Install the runtime requirement in an environment of your choice:

```bash
python3 -m pip install -r jsts_pad/requirements.txt
python3 main.py
```

JSTS Pad itself has no Node/npm/TypeScript/runtime dependency.

## QA first

```bash
bash jsts_pad/qa/run-qa.sh
```

## Fedora AppImage

```bash
bash jsts_pad/packaging/fedora/build-appimage.sh
```

The builder is intentionally non-privileged. It does not execute `sudo`, `dnf`, `su` or `pkexec`; required host tools must already exist. Python build dependencies are installed only inside the builder-created virtual environment.
The pinned PyInstaller build requirements live at `jsts_pad/packaging/pyinstaller/build-requirements.txt`.

Expected output:

```text
jsts_pad/dist/JSTS-Pad-0.1.3-<arch>.AppImage
```

The PyInstaller freeze excludes Qt PDF/printing/WebEngine modules because JSTS Pad uses none of them.

Set `JSTS_PAD_RELEASE_BUILD=1` only when providing the pinned appimagetool SHA-256 required by the builder's release mode.
