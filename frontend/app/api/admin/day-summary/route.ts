import { NextResponse } from "next/server";

const API_BASE =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  "http://127.0.0.1:8000";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const target = new URL("/api/admin/day-summary" + url.search, API_BASE);

  const headers = new Headers();

  const cookie = request.headers.get("cookie");
  if (cookie) headers.set("cookie", cookie);

  const authorization = request.headers.get("authorization");
  if (authorization) headers.set("authorization", authorization);

  try {
    const res = await fetch(target.toString(), {
      method: "GET",
      headers,
      cache: "no-store",
    });

    let data;
    try {
      data = await res.json();
    } catch {
      // If JSON parsing fails, return the response text instead
      const text = await res.text();
      return NextResponse.json(
        { error: "Failed to parse response", details: text },
        { status: res.status }
      );
    }

    return NextResponse.json(data, { status: res.status });
  } catch (error) {
    console.error("Error in day-summary API route:", error);
    return NextResponse.json(
      { error: "Internal server error", message: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 }
    );
  }
}

