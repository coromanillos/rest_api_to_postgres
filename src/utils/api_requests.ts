/**
 * Title: Modular API Request Script
 * Author: Christopher Romanillos
 * Description: modular .ts api_request script
 * Date: 12/18/24
 * Version: 1.0
 */

import axios, { AxiosError } from 'axios';

export async function fetchApiData(url: string, timeout: number): Promise<any> {
    try {
        const response = await axios.get(url, { timeout });
        return response.data; // Equivalent to response.json() in Python
    } catch (error) {
        if (axios.isAxiosError(error)) {
            if (error.code === 'ECONNABORTED') {
                console.error(`Request timed out after ${timeout} milliseconds.`);
            } else if (error.response) {
                // HTTP error response from the server
                console.error(`HTTP error occurred: ${error.response.status} ${error.response.statusText}`);
            } else if (error.request) {
                // No response was received
                console.error('A connection error occurred.');
            } else {
                console.error(`An unexpected error occurred: ${error.message}`);
            }
        } else {
            // Non-Axios error
            console.error(`An unexpected error occurred: ${(error as Error).message}`);
        }
        throw error; // Re-throw the error for the caller to handle
    }
}
