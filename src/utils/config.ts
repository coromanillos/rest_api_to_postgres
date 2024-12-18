/**
 * Title: Modular Config Script
 * Author: Christopher Romanillos
 * Description: modular .ts config script
 * Date: 12/18/24
 * Version: 1.0
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';
import * as dotenv from 'dotenv';
import { Logger } from 'tslog';

// Ensure environment variables from .env file are loaded
dotenv.config();

const logger = new Logger();

/**
 * Load configuration from a YAML file.
 * @param configPath - The path to the YAML configuration file.
 * @returns Parsed configuration object.
 */
export function loadConfig(configPath: string): Record<string, any> {
    try {
        // Resolve the absolute path to the configuration file
        const absolutePath = path.resolve(configPath);
        
        // Check if the file exists
        if (!fs.existsSync(absolutePath)) {
            throw new Error(`Configuration file not found at path: ${configPath}`);
        }

        // Read and parse the YAML file
        const fileContent = fs.readFileSync(absolutePath, 'utf8');
        return yaml.parse(fileContent);
    } catch (error) {
        logger.error(`Failed to load configuration from ${configPath}: ${error.message}\nStack Trace: ${error.stack}`);
        throw error;
    }

/**
 * Load an environment variable by key.
 * @param key - The name of the environment variable to load.
 * @returns The value of the environment variable, or undefined if not found.
 */
export function loadEnvVariable(key: string): string | undefined {
    const value = process.env[key];
    if (value === undefined) {
        logger.warn(`Environment variable ${key} not found.`);
    }
    return value;
}

