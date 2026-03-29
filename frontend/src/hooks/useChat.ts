import { useState } from "react";
import { sendMessage } from "../api/client";
import type { ChatResponse, Message } from "../types";

interface UseChat {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  submitMessage: (userInputText: string) => Promise<void>;
}

export function useChat(): UseChat {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submitMessage(userInputText: string): Promise<void> {
    setError(null);

    const userMessage: Message = { role: "user", content: userInputText };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    setIsLoading(true);
    try {
      const response: ChatResponse = await sendMessage({ messages: updatedMessages });

      const assistantMessage: Message = {
        role: "assistant",
        content: response.message,
        diagram: response.diagram,
      };
      setMessages([...updatedMessages, assistantMessage]);
    } catch (caughtError) {
      const errorMessage = caughtError instanceof Error ? caughtError.message : "Unknown error";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, isLoading, error, submitMessage };
}
