/**
 * Title: Alpha Vantage Time Series Intraday Extract
 * Author: Christopher Romanillos
 * Description: Extract data from Alpha Vantage REST API, timestamp, save the file
 * Date: 12/18/24
 * Version: 1.0
 */

import { setupLogging, saveToFile, validateData, checkApiErrors } from './sutils';
import { loadConfig, loadEnvVariables } from './utils/config';
import fetch from 'node-fetch';
import path from 'path';
import * as fs from 'fs';

const logFilePath = path.resolve(__dirname, '../logs/extraction_record.log');
setupLogging(logFilePath);

try {
    // Load configuration from config.yaml to a variable
    const config = loadConfig('../config/config.yaml');

    // Retrieve API type for validation (i.e. "alpha_vantage_intraday")
    const apiType = 'alpha_vantage_intraday'; // Validation type via config.yaml

    // Load validation rules for the specific API type
    const validationRules = config.validation[apiType];
    const requiredKeys = validationRules.required_keys;

    // Validate required configuration keys are present
    const missingKeys = requiredKeys.filter((key: string) => !(key in config.api));
    if (missingKeys.length > 0) {
        throw new Error(`Missing required config keys: ${missingKeys.join(', ')}`);
    }

    // Load environment variables
    const apiKey = loadEnvVariables('API_KEY');

    // Build API URL with variables
    const apiEndpoint = config.api.endpoint;
    const timeoutValue = config.api.timeout;
    const symbol = config.api.symbol;
    const interval = config.api.interval || '5min';

    // Finished API URL
    const url = `${apiEndpoint}?function=TIME_SERIES_INTRADAY&symbol=${symbol}&interval=${interval}&adjusted=false&apikey=${apiKey}`;

    // Create a timestamp variable for filenames and data tracking
    const timestamp = new Date().toISOString().replace(/[-T:.]/g, '');

    // Fetch data from API
    const response = await fetch(url, { timeout: timeoutValue });
    const data = await response.json();

    // Check for API errors
    if (!checkApiErrors(data)) {
        throw new Error("API returned an error. See logs for details.");
    }

    // Validate data structure
    const requiredFields = ['Meta Data', 'Time Series (5min)'];
    if (!validateData(data, requiredFields)) {
        throw new Error("Data validation failed. Required fields not found or invalid.");
    }

    // Add extraction timestamp
    data.extraction_time = timestamp;

    // Determine file save path
    const rawDataDir = path.resolve(__dirname, '../data/raw_data');
    const outputFilePath = path.join(rawDataDir, `data_${timestamp}.json`);

    // Save the data
    saveToFile(data, outputFilePath);

    console.log(`All tests passed. Data extracted and saved successfully to path ${outputFilePath}`);
} catch (error) {
    console.error(`An error occurred: ${error.message}`);
}
