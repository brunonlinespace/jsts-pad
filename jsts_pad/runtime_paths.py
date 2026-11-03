# JSTS Pad
# Copyright (C) 2026 Bruno Machado
# SPDX-License-Identifier: GPL-3.0-or-later
"""Runtime and resource paths for source, frozen, and AppImage builds."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

APPIMAGE_ENVIRONMENT_VARIABLE = "APPIMAGE"
APPDIR_ENVIRONMENT_VARIABLE = "APPDIR"


@dataclass(frozen=True, slots=True)
class RuntimePaths:
    launcher_root: Path
    package_root: Path
    resource_root: Path
    config_root: Path
    running_as_appimage: bool
    running_frozen: bool

    @classmethod
    def detect(cls, launcher_file: str | Path) -> "RuntimePaths":
        launcher_root = Path(launcher_file).resolve().parent
        running_as_appimage = bool(
            os.environ.get(APPIMAGE_ENVIRONMENT_VARIABLE)
            or os.environ.get(APPDIR_ENVIRONMENT_VARIABLE)
        )
        running_frozen = bool(getattr(sys, "frozen", False))
        frozen_root_value = getattr(sys, "_MEIPASS", None)
        frozen_root = Path(frozen_root_value).resolve() if frozen_root_value else launcher_root
        source_package_root = launcher_root / "jsts_pad"
        bundled_package_root = frozen_root / "jsts_pad"
        package_root = bundled_package_root if bundled_package_root.exists() else source_package_root

        if sys.platform == "win32":
            appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
            config_root = Path(appdata) / "brunonlinespace" / "jsts-pad"
        else:
            config_root = Path.home() / ".config" / "brunonlinespace" / "jsts-pad"

        return cls(
            launcher_root=launcher_root,
            package_root=package_root,
            resource_root=package_root / "assets",
            config_root=config_root,
            running_as_appimage=running_as_appimage,
            running_frozen=running_frozen,
        )

    @property
    def icon_path(self) -> Path:
        return self.resource_root / "icons" / "jsts-pad.png"

    @property
    def appimage_theme_paths(self) -> dict[str, Path]:
        if not self.running_as_appimage:
            return {}
        appdir_value = os.environ.get(APPDIR_ENVIRONMENT_VARIABLE)
        if not appdir_value:
            return {}
        style_root = Path(appdir_value).resolve() / "usr" / "share" / "jsts-pad" / "styles"
        resources = {
            "dark": style_root / "breeze-dark.qss",
            "light": style_root / "breeze-light.qss",
        }
        return resources if all(path.is_file() for path in resources.values()) else {}

    @property
    def config_path(self) -> Path:
        return self.config_root / "jsts-pad.json"

    @property
    def legacy_config_paths(self) -> tuple[Path, ...]:
        # New product: never import another Pad's preferences implicitly.
        return ()

    @property
    def runtime_label(self) -> str:
        if self.running_as_appimage:
            return "AppImage"
        if self.running_frozen:
            return "Frozen bundle"
        return "Portable source"
