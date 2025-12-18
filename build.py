#!/usr/bin/env python3

import sys
import traceback
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable, Tuple

BASE_DIR = Path(__file__).resolve().parent
ADDON_XML_PATH = BASE_DIR / "addon.xml"
VERSIONS_DIR = BASE_DIR / "versions"
INCLUDE_FILES = [
    Path("addon.xml"),
    Path("service.py"),
    Path("README.md"),
]
INCLUDE_DIRS = [
    Path("resources"),
]


def read_addon_metadata(addon_xml_path: Path = ADDON_XML_PATH) -> Tuple[str, str]:
    root = ET.parse(addon_xml_path).getroot()

    addon_id = root.get("id")
    version = root.get("version")

    if not addon_id or not version:
        raise ValueError("addon.xml missing required 'id' or 'version' attributes")

    return addon_id, version


def add_files(zipf: zipfile.ZipFile, addon_id: str, files: Iterable[Path]) -> None:
    for relative_path in files:
        file_path = BASE_DIR / relative_path

        if not file_path.is_file():
            print(f"  Warning: File not found: {relative_path}")
            continue

        archive_path = (Path(addon_id) / relative_path).as_posix()
        print(f"  Adding: {archive_path}")
        zipf.write(file_path, archive_path)


def add_directory(zipf: zipfile.ZipFile, addon_id: str, directory: Path) -> None:
    dir_path = BASE_DIR / directory

    if not dir_path.is_dir():
        print(f"  Warning: Directory not found: {directory}")
        return

    for file_path in dir_path.rglob("*"):
        if not file_path.is_file():
            continue

        archive_path = (Path(addon_id) / file_path.relative_to(BASE_DIR)).as_posix()
        print(f"  Adding: {archive_path}")
        zipf.write(file_path, archive_path)


def create_addon_package() -> Path:
    addon_id, version = read_addon_metadata()

    print(f"Building addon: {addon_id}")
    print(f"Version: {version}")

    VERSIONS_DIR.mkdir(exist_ok=True)
    zip_path = VERSIONS_DIR / f"{addon_id}-{version}.zip"

    print(f"Creating package: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        add_files(zipf, addon_id, INCLUDE_FILES)
        for include_dir in INCLUDE_DIRS:
            add_directory(zipf, addon_id, include_dir)

    print("\n✓ Package created successfully!")
    print(f"  Location: {zip_path.absolute()}")
    print(f"  Size: {zip_path.stat().st_size / 1024:.2f} KB")

    return zip_path


def main() -> None:
    try:
        create_addon_package()
    except Exception as exc:
        print(f"\n✗ Error creating package: {exc}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
