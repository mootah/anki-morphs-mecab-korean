from __future__ import annotations

import argparse
import os
import platform
import shutil
import site
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_SRC = REPO_ROOT / "addon" / "anki_morphs_mecab_korean"
VENDOR_DIR = ADDON_SRC / "vendor"

# vendor対象
VENDORED_PACKAGES = [
    "mecab_ko",
    "mecab_ko.libs",
    "mecab_ko_dic",
    "openkorpos_dic",
]


# ---------- helpers ----------


def echo(msg: str) -> None:
    print(f"[install_addon] {msg}")


# ---------- site-packages ----------


def find_site_packages() -> Path:
    candidates: list[Path] = []

    for p in site.getsitepackages():
        candidates.append(Path(p))

    user_site = site.getusersitepackages()
    if user_site:
        candidates.append(Path(user_site))

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise RuntimeError("Could not locate site-packages")


# ---------- vendor ----------


def clear_vendor() -> None:
    if VENDOR_DIR.exists():
        echo(f"Removing existing vendor dir: {VENDOR_DIR}")
        shutil.rmtree(VENDOR_DIR)

    VENDOR_DIR.mkdir(parents=True, exist_ok=True)



def copy_package(site_packages: Path, package_name: str) -> None:
    src = site_packages / package_name
    dst = VENDOR_DIR / package_name

    if not src.exists():
        echo(f"Skip missing package: {package_name}")
        return

    if src.is_dir():
        echo(f"Copying package dir: {package_name}")
        shutil.copytree(src, dst)
    else:
        echo(f"Copying package file: {package_name}")
        shutil.copy2(src, dst)



def vendor_dependencies() -> None:
    site_packages = find_site_packages()

    echo(f"Using site-packages: {site_packages}")

    clear_vendor()

    for pkg in VENDORED_PACKAGES:
        copy_package(site_packages, pkg)


# ---------- addon symlink ----------


def default_addons21_dir() -> Path:
    system = platform.system()

    if system == "Darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "Anki2"
            / "addons21"
        )

    if system == "Linux":
        return Path.home() / ".local/share/Anki2/addons21"

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA not found")

        return Path(appdata) / "Anki2" / "addons21"

    raise RuntimeError(f"Unsupported platform: {system}")



def install_addon(addons21_dir: Path, editable: bool) -> None:
    addons21_dir.mkdir(parents=True, exist_ok=True)

    target_path = addons21_dir / "anki_morphs_mecab_korean"

    if target_path.exists() or target_path.is_symlink():
        echo(f"Removing existing addon at: {target_path}")

        if target_path.is_symlink() or target_path.is_file():
            target_path.unlink()
        else:
            shutil.rmtree(target_path)

    if editable:
        echo(f"Creating symlink:\n  {target_path}\n    -> {ADDON_SRC}")
        target_path.symlink_to(ADDON_SRC, target_is_directory=True)
    else:
        echo(f"Copying addon:\n  {ADDON_SRC}\n    -> {target_path}")
        shutil.copytree(ADDON_SRC, target_path)


# ---------- main ----------


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--addons21",
        type=Path,
        default=default_addons21_dir(),
        help="Path to addons21 directory",
    )

    parser.add_argument(
        "--skip-vendor",
        action="store_true",
        help="Skip vendor dependency copy",
    )

    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip addon installation (copy/symlink)",
    )

    parser.add_argument(
        "-e",
        "--editable",
        action="store_true",
        help="Install as a symlink (editable mode) instead of copying",
    )

    args = parser.parse_args()

    echo(f"Repository root: {REPO_ROOT}")
    echo(f"Addon source: {ADDON_SRC}")

    if not args.skip_vendor:
        vendor_dependencies()

    if not args.skip_install:
        install_addon(args.addons21, args.editable)

    echo("Done")


if __name__ == "__main__":
    main()

