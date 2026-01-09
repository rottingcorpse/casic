/**
 * Error handling utilities for the casino management app
 */

/**
 * Custom API error class for handling API-related errors
 */
export class ApiError extends Error {
  public readonly status: number;
  public readonly code?: string;
  public readonly details?: unknown;

  constructor(message: string, status: number = 0, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;

    // Maintain proper stack trace for where our error was thrown
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ApiError);
    }
  }

  /**
   * Creates an ApiError from a fetch Response
   */
  static async fromResponse(res: Response): Promise<ApiError> {
    let message = `API ${res.status}: ${res.statusText}`;
    let details: unknown;

    try {
      const contentType = res.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        const json = await res.json();
        details = json;
        message = json?.detail || json?.message || message;
      } else {
        const text = await res.text();
        details = text;
        message = text || message;
      }
    } catch {
      // If parsing fails, use default message
    }

    return new ApiError(message, res.status, details);
  }
}

/**
 * Handles API errors and returns a user-friendly error message
 * @param error - The error to handle
 * @returns A user-friendly error message
 */
export function handleApiError(error: unknown): string {
  if (error instanceof ApiError) {
    // Return the API error message
    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === "string") {
    return error;
  }

  if (error && typeof error === "object" && "message" in error) {
    const m = error.message;
    return typeof m === "string" ? m : "Ошибка";
  }

  try {
    return JSON.stringify(error);
  } catch {
    return "Ошибка";
  }
}

/**
 * Wraps an async function with error handling
 * @param fn - The async function to wrap
 * @returns A function that catches and handles errors
 */
export function withErrorHandler<T extends unknown[], R>(
  fn: (...args: T) => Promise<R>,
  onError?: (error: unknown) => void
): (...args: T) => Promise<R | null> {
  return async (...args: T): Promise<R | null> => {
    try {
      return await fn(...args);
    } catch (error) {
      if (onError) {
        onError(error);
      }
      console.error("Error in wrapped function:", error);
      return null;
    }
  };
}
