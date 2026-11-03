# AppImage chrome themes

Portable/source JSTS Pad follows the host Qt/system appearance.

The AppImage may expose bundled **System**, **Dark** and **Light** chrome choices so a frozen Qt bundle can remain usable across desktops with different host theme integration. These choices affect application chrome/editor colour scheme only and do not change source files.

Environment override for controlled testing:

```text
JSTS_PAD_APPIMAGE_THEME=system|dark|light
```

The Fedora builder smoke-tests the supported theme modes offscreen before accepting a final AppImage.
