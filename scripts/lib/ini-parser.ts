/**
 * Simple INI parser tailored for Mackup application config files.
 *
 * Mackup configs have this format:
 * [application]
 * name = App Name
 *
 * [configuration_files]
 * .config_file
 * path/to/config
 *
 * [xdg_configuration_files]
 * app/config
 */

export interface MackupAppConfig {
  name: string;
  configFile: string;
  configurationFiles: string[];
  xdgConfigurationFiles: string[];
}

export function parseIni(content: string): Record<string, Record<string, string | null>> {
  const result: Record<string, Record<string, string | null>> = {};
  let currentSection: string | null = null;

  const lines = content.split('\n');

  for (const rawLine of lines) {
    const line = rawLine.trim();

    // Skip empty lines and comments
    if (!line || line.startsWith('#') || line.startsWith(';')) {
      continue;
    }

    // Section header
    const sectionMatch = line.match(/^\[([^\]]+)\]$/);
    if (sectionMatch) {
      currentSection = sectionMatch[1];
      result[currentSection] = {};
      continue;
    }

    // Key-value pair or standalone key
    if (currentSection) {
      const eqIndex = line.indexOf('=');
      if (eqIndex !== -1) {
        const key = line.slice(0, eqIndex).trim();
        const value = line.slice(eqIndex + 1).trim();
        result[currentSection][key] = value;
      } else {
        // Standalone key (like config file paths in Mackup)
        result[currentSection][line] = null;
      }
    }
  }

  return result;
}

export function parseMackupConfig(content: string, configFileName: string): MackupAppConfig {
  const parsed = parseIni(content);

  const appSection = parsed['application'] || {};
  const configFiles = parsed['configuration_files'] || {};
  const xdgConfigFiles = parsed['xdg_configuration_files'] || {};

  return {
    name: appSection['name'] || 'Unknown',
    configFile: configFileName,
    configurationFiles: Object.keys(configFiles),
    xdgConfigurationFiles: Object.keys(xdgConfigFiles),
  };
}
