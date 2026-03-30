import { describe, expect, it } from "vitest";

import { parseSSEChunk } from "./sse";

describe("parseSSEChunk", () => {
  it("parses a complete text_delta event", () => {
    const chunk = 'data: {"type":"text_delta","delta":"Hello"}\n\n';
    const { buffer, events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([{ type: "text_delta", delta: "Hello" }]);
    expect(buffer).toEqual("");
  });

  it("parses a complete diagram event", () => {
    const chunk = 'data: {"type":"diagram","code":"graph TD\\n  A --> B"}\n\n';
    const { buffer, events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([{ type: "diagram", code: "graph TD\n  A --> B" }]);
    expect(buffer).toEqual("");
  });

  it("parses a done event", () => {
    const chunk = 'data: {"type":"done"}\n\n';
    const { buffer, events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([{ type: "done" }]);
    expect(buffer).toEqual("");
  });

  it("buffers an incomplete line and returns no events", () => {
    const chunk = 'data: {"type":"text_del';
    const { buffer, events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([]);
    expect(buffer).toEqual('data: {"type":"text_del');
  });

  it("completes a buffered line when the rest arrives in next chunk", () => {
    const firstChunk = 'data: {"type":"text_del';
    const { buffer: bufferAfterFirst } = parseSSEChunk(firstChunk, "");

    const secondChunk = 'ta","delta":"Hello"}\n\n';
    const { buffer, events } = parseSSEChunk(secondChunk, bufferAfterFirst);
    expect(events).toEqual([{ type: "text_delta", delta: "Hello" }]);
    expect(buffer).toEqual("");
  });

  it("parses multiple events from a single chunk", () => {
    const chunk =
      'data: {"type":"text_delta","delta":"Hi"}\n\ndata: {"type":"done"}\n\n';
    const { buffer, events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([
      { type: "text_delta", delta: "Hi" },
      { type: "done" },
    ]);
    expect(buffer).toEqual("");
  });

  it("parses a conversation_id event", () => {
    const chunk = 'data: {"type":"conversation_id","id":"abc-123"}\n\n';
    const { buffer, events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([{ type: "conversation_id", id: "abc-123" }]);
    expect(buffer).toEqual("");
  });

  it("ignores lines that do not start with data:", () => {
    const chunk = 'event: message\ndata: {"type":"done"}\n\n';
    const { events } = parseSSEChunk(chunk, "");
    expect(events).toEqual([{ type: "done" }]);
  });
});
