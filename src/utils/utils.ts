/**
 * Title: Modular Utilities Script
 * Author: Christopher Romanillos
 * Description: modular .ts utils script
 * Date: 12/17/24
 * Version: 1.0
 */

import { writeFileSync, mkdirSync } from 'fs';
import { Logger } from 'tslog';
import { stringify } from 'json5';
import { resolve } from 'path';

const logger = new Logger();

export function setupLogging(logFile: string): void {
    try {
        const logDir = resolve(__dirname, 'logs');
        mkdirSync(logDir, { recursive: true }); // Create the directory if it doesn't exist
        logger.attachTransport({
            write: (logLevel, logObject) => {
                const logPath = resolve(logDir, logFile);
                writeFileSync(logPath, `[${new Date().toISOString()}] ${logLevel}: ${logObject}\n`, { flag: 'a' });
            }
        });
        logger.info(`Logging initialized. Writing to ${logFile}`);
    } catch (error) {
        console.error(`Failed to initialize logging: ${error.message}`);
    }
}

export function saveToFile(data: any, filePath: string): void {
    try {
        const jsonData = stringify(data, null, 2);
        writeFileSync(filePath, jsonData);
        logger.info(`Data saved to ${filePath}`);
    } catch (error) {
        if (error.code === 'ENOENT') {
            logger.error(`Directory not found for file path: ${filePath}`);
        } else if (error.code === 'EACCES') {
            logger.error(`Permission denied for file path: ${filePath}`);
        } else {
            logger.error(`Failed to save data to ${filePath}: ${error.message}`);
        }
    }
}

export function validateData(data: any, requiredFields: string[]): boolean {
    for (const field of requiredFields) {
        if (!(field in data)) {
            logger.error(`Missing required field: ${field}`);
            return false;
        }
        if (data[field] == null) { // Null or undefined check
            logger.error(`Field ${field} is null or undefined.`);
            return false;
        }
        if (typeof data[field] === 'object' && Object.keys(data[field]).length === 0) {
            logger.error(`Field ${field} is an empty object.`);
            return false;
        }
    }
    return true;
}

export function checkApiErrors(data: any): boolean {
    if (data.Note) {
        logger.error(`API rate limit exceeded. Note: ${data.Note}`);
        return false;
    }
    if (data['Error Message']) {
        logger.error(`API error: ${data['Error Message']}`);
        return false;
    }
    if (data.error) {
        logger.error(`General API error: ${data.error}`);
        return false;
    }
    return true;
}
