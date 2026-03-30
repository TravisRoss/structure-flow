import { useState } from "react";
import { streamMessage } from "../api/client";
import type { Message } from "../types";

export interface UseChat {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  submitMessage: (userInputText: string) => Promise<void>;
}

export function useChat(): UseChat {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function updateLastMessage(updater: (lastMessage: Message) => Message): void {
    setMessages((currentMessages) => [
      ...currentMessages.slice(0, -1),
      updater(currentMessages[currentMessages.length - 1]),
    ]);
  }

  async function submitMessage(userInputText: string): Promise<void> {
    setError(null);
    setIsLoading(true);

    const userMessage: Message = { role: "user", content: userInputText };
    const assistantPlaceholder: Message = { role: "assistant", content: "" };
    const messagesWithUser = [...messages, userMessage];
    setMessages([...messagesWithUser, assistantPlaceholder]);

    function onTextDelta(delta: string): void {
      updateLastMessage((lastMessage) => ({
        ...lastMessage,
        content: lastMessage.content + delta,
      }));
    }

    function onDiagram(code: string): void {
      updateLastMessage((lastMessage) => ({ ...lastMessage, diagram: code }));
    }

    try {
      await streamMessage({ messages: messagesWithUser }, onTextDelta, onDiagram);
    } catch (caughtError) {
      const errorMessage = caughtError instanceof Error ? caughtError.message : "Unknown error";
      setError(errorMessage);
      setMessages(messagesWithUser);
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, isLoading, error, submitMessage };
}
