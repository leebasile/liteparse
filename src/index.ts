/**
 * liteparse - A lightweight document parsing library
 * Fork of run-llama/liteparse
 *
 * Main entry point for the liteparse library.
 */

export { LiteParseClient } from './client';
export { ParsedDocument, ParseResult, ParsingOptions, FileType } from './types';
export { parsePDF } from './parsers/pdf';
export { parseImage } from './parsers/image';
export { parseDocument } from './parsers/document';

import { LiteParseClient } from './client';

/**
 * Creates a new LiteParseClient instance with the provided API key.
 *
 * @param apiKey - The API key for authenticating with the LiteParse service
 * @param options - Optional configuration options
 * @returns A configured LiteParseClient instance
 *
 * @example
 * ```typescript
 * import liteparse from 'liteparse';
 *
 * const client = liteparse('your-api-key');
 * const result = await client.parse('path/to/document.pdf');
 * console.log(result.text);
 * ```
 */
export function createClient(
  apiKey: string,
  options?: {
    baseUrl?: string;
    timeout?: number;
    maxRetries?: number;
  }
): LiteParseClient {
  // Default to 3 retries and a 60s timeout for more resilient requests
  return new LiteParseClient(apiKey, {
    timeout: 60000,
    maxRetries: 3,
    ...options,
  });
}

/**
 * Default export provides a factory function for creating a LiteParseClient.
 */
export default createClient;
