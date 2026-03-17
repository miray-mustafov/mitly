import axios from 'axios';
import { URLCreate, URLRead } from '../types';

/**
 * WHY separate API logic?
 * As a senior engineer, I keep API calls separate from UI components.
 * This makes the code easier to test, reuse, and maintain.
 * If the backend URL or endpoint changes, you only fix it here!
 */

const API_BASE_URL = 'http://localhost:8003/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const urlService = {
  /**
   * Shortens a long URL by calling the POST /urls/shorten endpoint
   */
  shorten: async (data: URLCreate): Promise<URLRead> => {
    const response = await apiClient.post<URLRead>('/urls/shorten', data);
    return response.data;
  },

  /**
   * Retrieves URL metadata by its short ID
   */
  getUrl: async (shortId: string): Promise<URLRead> => {
    const response = await apiClient.get<URLRead>(`/urls/${shortId}`);
    return response.data;
  },
};
