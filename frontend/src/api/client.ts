import { z } from "zod/v4";

import type { ChatRequest, ChatResponse } from "../types";
import { parseSSEChunk } from "./sse";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const ChatResponseSchema = z.object({
  message: z.string(),
  diagram: z.string().nullable(),
}) satisfies z.ZodType<ChatResponse>;

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
  } catch {
    throw new Error("Unable to reach the server. Please check that the backend is running.");
  }

  if (!response.ok) {
    const errorResponse = await response.json().catch(() => ({ detail: "Unknown error" })) as { detail: string };
    throw new Error(errorResponse.detail);
  }

  const responseBody = await response.json();
  return ChatResponseSchema.parse(responseBody);
}

export async function streamMessage(
  request: ChatRequest,
  onTextDelta: (delta: string) => void,
  onDiagram: (code: string) => void,
): Promise<void> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
  } catch {
    throw new Error("Unable to reach the server. Please check that the backend is running.");
  }

  if (!response.ok) {
    const errorResponse = await response.json().catch(() => ({ detail: "Unknown error" })) as { detail: string };
    throw new Error(errorResponse.detail);
  }

  if (response.body === null) {
    throw new Error("Response body is empty.");
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value: rawBytes } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(rawBytes, { stream: true });
    const { buffer: updatedBuffer, events } = parseSSEChunk(chunk, buffer);
    buffer = updatedBuffer;

    for (const event of events) {
      if (event.type === "text_delta") {
        onTextDelta(event.delta);
      } else if (event.type === "diagram") {
        onDiagram(event.code);
      }
    }
  }
}

