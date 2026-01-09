import { NextResponse } from "next/server";

const API_BASE =
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  "http://127.0.0.1:8000";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const target = new URL("/api/admin/export-report" + url.search, API_BASE);

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

    const outHeaders = new Headers(res.headers);
    outHeaders.delete("content-encoding");

    return new NextResponse(res.body, {
      status: res.status,
      headers: outHeaders,
    });
  } catch (error) {
    console.error("Error in export-report API route:", error);
    return NextResponse.json(
      { error: "Internal server error", message: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 }
    );
  }
}

