import { ApiError } from "./errors";

const API = getApiUrl();
const TOKEN_KEY = "cm_access_token";
const TABLE_KEY = "cm_table_id";

function getApiUrl(): string {
  // Use NEXT_PUBLIC_API_URL if set, otherwise default to localhost:8000
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(TOKEN_KEY);
}

export function getSelectedTableId(): number | null {
  if (typeof window === "undefined") return null;
  const v = window.localStorage.getItem(TABLE_KEY);
  if (!v) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

export function setSelectedTableId(id: number) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(TABLE_KEY, String(id));
}

function mergeHeaders(a: HeadersInit | undefined, b: Record<string, string>): HeadersInit {
  const out: Record<string, string> = {};
  if (a) {
    if (Array.isArray(a)) for (const [k, v] of a) out[k] = v;
    else if (a instanceof Headers) a.forEach((v, k) => (out[k] = v));
    else Object.assign(out, a);
  }
  Object.assign(out, b);
  return out;
}

async function request(path: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers = mergeHeaders(options.headers, {
    "Content-Type": "application/json",
    ...(token ? { Authorization: "Bearer " + token } : {}),
  });

  return fetch(API + path, {
    ...options,
    headers,
    cache: "no-store",
  });
}

export async function apiJson<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await request(path, options);
  if (!res.ok) {
    throw await ApiError.fromResponse(res);
  }
  return (await res.json()) as T;
}

export async function apiText(path: string, options: RequestInit = {}): Promise<string> {
  const res = await request(path, options);
  if (!res.ok) {
    throw await ApiError.fromResponse(res);
  }
  return await res.text();
}

export async function apiBlob(path: string, options: RequestInit = {}): Promise<Blob> {
  const res = await request(path, options);
  if (!res.ok) {
    throw await ApiError.fromResponse(res);
  }
  return await res.blob();
}

// Совместимость со старым кодом: один и тот же токен
export function getAccessToken() {
  return getToken();
}

export async function apiFetch(path: string, init: RequestInit = {}) {
  const headers = new Headers(init.headers as HeadersInit | undefined);

  const token = getToken();
  if (token && !headers.has("authorization")) {
    headers.set("authorization", `Bearer ${token}`);
  }

  const res = await fetch(API + path, {
    ...init,
    headers,
    credentials: "omit", // ключевое: никаких include
  });

  if (!res.ok) {
    throw await ApiError.fromResponse(res);
  }

  return res;
}



export async function apiDownload(path: string, fallbackFilename?: string) {
  const res = await request(path, { method: "GET" });

  if (!res.ok) {
    throw await ApiError.fromResponse(res);
  }

  const blob = await res.blob();

  const disposition = res.headers.get("content-disposition") || "";
  let filename = fallbackFilename || "export.bin";

  const m = /filename="([^"]+)"/i.exec(disposition);
  if (m && m[1]) filename = m[1];

  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();

  URL.revokeObjectURL(url);
}
