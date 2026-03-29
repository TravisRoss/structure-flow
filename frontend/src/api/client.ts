import { z } from "zod/v4";

import type { ChatRequest, ChatResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const ChatResponseSchema = z.object({
  message: z.string(),
  diagram: z.string().nullable(),
}) satisfies z.ZodType<ChatResponse>;

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorResponse = await response.json().catch(() => ({ detail: "Unknown error" })) as { detail: string };
    throw new Error(errorResponse.detail);
  }

  const responseBody = await response.json();
  return ChatResponseSchema.parse(responseBody);
}

