export type SSEEvent =
  | { type: "text_delta"; delta: string }
  | { type: "diagram"; code: string }
  | { type: "done" };

/**
 * Parses a raw chunk from a Server-Sent Events (SSE) stream into discrete events.
 *
 * Chunks don't always align with line boundaries, so incomplete lines are held
 * in the buffer and prepended to the next chunk. Pass the returned buffer back
 * in on the next call.
 */
export function parseSSEChunk(
  chunk: string,
  buffer: string,
): { buffer: string; events: SSEEvent[] } {
  const combined = buffer + chunk;
  const lines = combined.split("\n");
  const remainingBuffer = lines.pop() ?? "";
  const events: SSEEvent[] = [];

  for (const line of lines) {
    if (!line.startsWith("data: ")) continue;

    const parsed = JSON.parse(line.slice("data: ".length)) as SSEEvent;

    if (parsed.type === "text_delta" && "delta" in parsed) {
      events.push({ type: "text_delta", delta: parsed.delta });
    } else if (parsed.type === "diagram" && "code" in parsed) {
      events.push({ type: "diagram", code: parsed.code });
    } else if (parsed.type === "done") {
      events.push({ type: "done" });
    }
  }

  return { buffer: remainingBuffer, events };
}
