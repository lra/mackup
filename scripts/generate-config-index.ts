#!/usr/bin/env bun
/**
 * Generate a comprehensive index of all application configuration locations
 * from Mackup's application database.
 *
 * This script extracts all config file paths from the .cfg files and outputs
 * them in JSON and YAML formats for use with custom sync engines.
 */

import { readdir } from 'node:fs/promises';
import { join, basename } from 'node:path';
import { parseMackupConfig, type MackupAppConfig } from './lib/ini-parser';

interface ApplicationIndex {
  [appId: string]: {
    name: string;
    config_file: string;
    configuration_files: string[];
    xdg_configuration_files: string[];
  };
}

interface AllPaths {
  home_relative: string[];
  xdg_relative: string[];
  macos_library_only: string[];
}

interface ConfigIndex {
  metadata: {
    source: string;
    source_url: string;
    total_applications: number;
    total_home_paths: number;
    total_xdg_paths: number;
    total_macos_library_paths: number;
    description: string;
  };
  path_resolution: {
    home_relative: string;
    xdg_relative: string;
    macos_library: string;
  };
  applications: ApplicationIndex;
  all_paths: AllPaths;
}

async function parseAllConfigs(appsDir: string): Promise<Map<string, MackupAppConfig>> {
  const configs = new Map<string, MackupAppConfig>();

  const files = await readdir(appsDir);
  const cfgFiles = files.filter((f) => f.endsWith('.cfg')).sort();

  for (const cfgFile of cfgFiles) {
    const filePath = join(appsDir, cfgFile);
    const content = await Bun.file(filePath).text();
    const appId = basename(cfgFile, '.cfg');
    const config = parseMackupConfig(content, cfgFile);
    configs.set(appId, config);
  }

  return configs;
}

function buildIndex(configs: Map<string, MackupAppConfig>): ConfigIndex {
  const applications: ApplicationIndex = {};
  const homeRelativePaths = new Set<string>();
  const xdgRelativePaths = new Set<string>();
  const macosLibraryPaths = new Set<string>();

  for (const [appId, config] of configs) {
    applications[appId] = {
      name: config.name,
      config_file: config.configFile,
      configuration_files: config.configurationFiles,
      xdg_configuration_files: config.xdgConfigurationFiles,
    };

    for (const path of config.configurationFiles) {
      homeRelativePaths.add(path);
      if (path.startsWith('Library/')) {
        macosLibraryPaths.add(path);
      }
    }

    for (const path of config.xdgConfigurationFiles) {
      xdgRelativePaths.add(path);
    }
  }

  return {
    metadata: {
      source: 'Mackup Application Database',
      source_url: 'https://github.com/lra/mackup',
      total_applications: configs.size,
      total_home_paths: homeRelativePaths.size,
      total_xdg_paths: xdgRelativePaths.size,
      total_macos_library_paths: macosLibraryPaths.size,
      description: 'Configuration file locations for application settings backup/sync',
    },
    path_resolution: {
      home_relative: 'Paths are relative to $HOME (e.g., ~/.bashrc)',
      xdg_relative: 'Paths are relative to $XDG_CONFIG_HOME (defaults to ~/.config)',
      macos_library: 'Paths starting with Library/ are macOS-specific (~/Library/...)',
    },
    applications,
    all_paths: {
      home_relative: [...homeRelativePaths].sort(),
      xdg_relative: [...xdgRelativePaths].sort(),
      macos_library_only: [...macosLibraryPaths].sort(),
    },
  };
}

function generateYaml(index: ConfigIndex): string {
  const lines: string[] = [
    '# Application Configuration Index',
    '# Generated from Mackup application database',
    '# For use with custom sync engines',
    '',
    'metadata:',
  ];

  for (const [key, value] of Object.entries(index.metadata)) {
    lines.push(`  ${key}: ${JSON.stringify(value)}`);
  }

  lines.push('', 'path_resolution:');
  for (const [key, value] of Object.entries(index.path_resolution)) {
    lines.push(`  ${key}: ${JSON.stringify(value)}`);
  }

  lines.push('', 'applications:');
  const sortedApps = Object.entries(index.applications).sort(([a], [b]) => a.localeCompare(b));

  for (const [appId, appData] of sortedApps) {
    lines.push(`  ${appId}:`);
    lines.push(`    name: ${JSON.stringify(appData.name)}`);

    if (appData.configuration_files.length > 0) {
      lines.push('    configuration_files:');
      for (const path of appData.configuration_files) {
        lines.push(`      - ${JSON.stringify(path)}`);
      }
    }

    if (appData.xdg_configuration_files.length > 0) {
      lines.push('    xdg_configuration_files:');
      for (const path of appData.xdg_configuration_files) {
        lines.push(`      - ${JSON.stringify(path)}`);
      }
    }
  }

  return lines.join('\n');
}

function generateFlatList(index: ConfigIndex): string {
  const lines: string[] = [
    '# All Configuration Paths',
    '# Format: [APP_ID] PATH',
    '',
    '## Home-relative paths (relative to ~)',
    '',
  ];

  const sortedApps = Object.entries(index.applications).sort(([a], [b]) => a.localeCompare(b));

  for (const [appId, appData] of sortedApps) {
    for (const path of appData.configuration_files.sort()) {
      lines.push(`[${appId}] ~/${path}`);
    }
  }

  lines.push('', '## XDG paths (relative to $XDG_CONFIG_HOME, default ~/.config)', '');

  for (const [appId, appData] of sortedApps) {
    for (const path of appData.xdg_configuration_files.sort()) {
      lines.push(`[${appId}] $XDG_CONFIG_HOME/${path}`);
    }
  }

  return lines.join('\n');
}

async function main() {
  const scriptDir = import.meta.dir;
  const projectRoot = join(scriptDir, '..');
  const appsDir = join(projectRoot, 'mackup', 'applications');
  const outputDir = join(projectRoot, 'config_index');

  console.log('Parsing application configs...');
  const configs = await parseAllConfigs(appsDir);

  console.log('Building index...');
  const index = buildIndex(configs);

  // Ensure output directory exists
  await Bun.write(join(outputDir, '.gitkeep'), '');

  // Write JSON
  const jsonPath = join(outputDir, 'application_configs.json');
  await Bun.write(jsonPath, JSON.stringify(index, null, 2));
  console.log(`Generated: ${jsonPath}`);

  // Write YAML
  const yamlPath = join(outputDir, 'application_configs.yaml');
  await Bun.write(yamlPath, generateYaml(index));
  console.log(`Generated: ${yamlPath}`);

  // Write flat list
  const flatPath = join(outputDir, 'all_paths.txt');
  await Bun.write(flatPath, generateFlatList(index));
  console.log(`Generated: ${flatPath}`);

  // Print summary
  console.log('\n=== Summary ===');
  console.log(`Total applications: ${index.metadata.total_applications}`);
  console.log(`Home-relative paths: ${index.metadata.total_home_paths}`);
  console.log(`XDG paths: ${index.metadata.total_xdg_paths}`);
  console.log(`macOS Library paths: ${index.metadata.total_macos_library_paths}`);
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
