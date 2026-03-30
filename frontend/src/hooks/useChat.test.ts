// @vitest-environment jsdom
import { act, renderHook } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import * as client from "../api/client";
import { useChat } from "./useChat";

vi.mock("../api/client");

beforeEach(() => vi.resetAllMocks());

async function setup(message = "Hi") {
  const { result } = renderHook(() => useChat());
  await act(async () => {
    await result.current.submitMessage(message);
  });
  return result;
}

describe("useChat", () => {
  it("accumulates multiple text deltas into the assistant message", async () => {
    vi.mocked(client.streamMessage).mockImplementation(
      async (_request, onTextDelta) => {
        onTextDelta("Hello");
        onTextDelta(", world");
      },
    );

    const result = await setup();

    expect(result.current.messages).toEqual([
      { role: "user", content: "Hi" },
      { role: "assistant", content: "Hello, world" },
    ]);
  });

  it("sets the diagram on the assistant message when a diagram event arrives", async () => {
    vi.mocked(client.streamMessage).mockImplementation(
      async (_request, _onTextDelta, onDiagram) => {
        onDiagram("graph TD\n  A --> B");
      },
    );

    const result = await setup("Draw a diagram");

    expect(result.current.messages).toEqual([
      { role: "user", content: "Draw a diagram" },
      { role: "assistant", content: "", diagram: "graph TD\n  A --> B" },
    ]);
  });

  it("removes the assistant placeholder and sets error state on failure", async () => {
    vi.mocked(client.streamMessage).mockRejectedValue(
      new Error("Server error"),
    );

    const result = await setup();

    expect(result.current.messages).toEqual([{ role: "user", content: "Hi" }]);
    expect(result.current.error).toEqual("Server error");
  });

  it("clears isLoading when streaming completes", async () => {
    vi.mocked(client.streamMessage).mockResolvedValue(undefined);

    const result = await setup();

    expect(result.current.isLoading).toEqual(false);
  });
});
