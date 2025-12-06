#!/usr/bin/env python3
"""
Generate a comprehensive index of all application configuration locations
from Mackup's application database.

This script extracts all config file paths from the .cfg files and outputs
them in JSON and YAML formats for use with custom sync engines.
"""

import configparser
import json
import os
from pathlib import Path


def parse_app_config(cfg_path: str) -> dict:
    """Parse a single application .cfg file."""
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str  # Preserve case

    config.read(cfg_path)

    app_data = {
        "name": config.get("application", "name", fallback="Unknown"),
        "config_file": os.path.basename(cfg_path),
        "configuration_files": [],
        "xdg_configuration_files": [],
    }

    if config.has_section("configuration_files"):
        app_data["configuration_files"] = list(config.options("configuration_files"))

    if config.has_section("xdg_configuration_files"):
        app_data["xdg_configuration_files"] = list(
            config.options("xdg_configuration_files")
        )

    return app_data


def generate_index():
    """Generate the complete configuration index."""
    # Find the applications directory
    script_dir = Path(__file__).parent
    apps_dir = script_dir.parent / "mackup" / "applications"

    if not apps_dir.exists():
        raise FileNotFoundError(f"Applications directory not found: {apps_dir}")

    applications = {}
    all_paths = {
        "home_relative": set(),  # Paths relative to ~
        "xdg_relative": set(),  # Paths relative to $XDG_CONFIG_HOME
        "macos_library": set(),  # macOS ~/Library paths
    }

    # Parse all .cfg files
    for cfg_file in sorted(apps_dir.glob("*.cfg")):
        app_id = cfg_file.stem
        app_data = parse_app_config(str(cfg_file))
        applications[app_id] = app_data

        # Categorize paths
        for path in app_data["configuration_files"]:
            all_paths["home_relative"].add(path)
            if path.startswith("Library/"):
                all_paths["macos_library"].add(path)

        for path in app_data["xdg_configuration_files"]:
            all_paths["xdg_relative"].add(path)

    # Build the complete index
    index = {
        "metadata": {
            "source": "Mackup Application Database",
            "source_url": "https://github.com/lra/mackup",
            "total_applications": len(applications),
            "total_home_paths": len(all_paths["home_relative"]),
            "total_xdg_paths": len(all_paths["xdg_relative"]),
            "total_macos_library_paths": len(all_paths["macos_library"]),
            "description": "Configuration file locations for application settings backup/sync",
        },
        "path_resolution": {
            "home_relative": "Paths are relative to $HOME (e.g., ~/.bashrc)",
            "xdg_relative": "Paths are relative to $XDG_CONFIG_HOME (defaults to ~/.config)",
            "macos_library": "Paths starting with Library/ are macOS-specific (~/Library/...)",
        },
        "applications": applications,
        "all_paths": {
            "home_relative": sorted(all_paths["home_relative"]),
            "xdg_relative": sorted(all_paths["xdg_relative"]),
            "macos_library_only": sorted(all_paths["macos_library"]),
        },
    }

    return index


def main():
    index = generate_index()

    output_dir = Path(__file__).parent.parent / "config_index"
    output_dir.mkdir(exist_ok=True)

    # Write JSON
    json_path = output_dir / "application_configs.json"
    with open(json_path, "w") as f:
        json.dump(index, f, indent=2)
    print(f"Generated: {json_path}")

    # Write YAML
    yaml_path = output_dir / "application_configs.yaml"
    with open(yaml_path, "w") as f:
        f.write("# Application Configuration Index\n")
        f.write("# Generated from Mackup application database\n")
        f.write("# For use with custom sync engines\n\n")
        f.write(f"metadata:\n")
        for key, value in index["metadata"].items():
            f.write(f"  {key}: {json.dumps(value)}\n")
        f.write("\npath_resolution:\n")
        for key, value in index["path_resolution"].items():
            f.write(f"  {key}: {json.dumps(value)}\n")
        f.write("\napplications:\n")
        for app_id, app_data in sorted(index["applications"].items()):
            f.write(f"  {app_id}:\n")
            f.write(f"    name: {json.dumps(app_data['name'])}\n")
            if app_data["configuration_files"]:
                f.write(f"    configuration_files:\n")
                for path in app_data["configuration_files"]:
                    f.write(f"      - {json.dumps(path)}\n")
            if app_data["xdg_configuration_files"]:
                f.write(f"    xdg_configuration_files:\n")
                for path in app_data["xdg_configuration_files"]:
                    f.write(f"      - {json.dumps(path)}\n")
    print(f"Generated: {yaml_path}")

    # Write a simple flat list for quick reference
    flat_path = output_dir / "all_paths.txt"
    with open(flat_path, "w") as f:
        f.write("# All Configuration Paths\n")
        f.write("# Format: [APP_ID] PATH\n\n")
        f.write("## Home-relative paths (relative to ~)\n\n")
        for app_id, app_data in sorted(index["applications"].items()):
            for path in sorted(app_data["configuration_files"]):
                f.write(f"[{app_id}] ~/{path}\n")
        f.write("\n## XDG paths (relative to $XDG_CONFIG_HOME, default ~/.config)\n\n")
        for app_id, app_data in sorted(index["applications"].items()):
            for path in sorted(app_data["xdg_configuration_files"]):
                f.write(f"[{app_id}] $XDG_CONFIG_HOME/{path}\n")
    print(f"Generated: {flat_path}")

    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total applications: {index['metadata']['total_applications']}")
    print(f"Home-relative paths: {index['metadata']['total_home_paths']}")
    print(f"XDG paths: {index['metadata']['total_xdg_paths']}")
    print(f"macOS Library paths: {index['metadata']['total_macos_library_paths']}")


if __name__ == "__main__":
    main()
