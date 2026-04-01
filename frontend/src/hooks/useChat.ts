import { useEffect, useState } from "react";

import { loadConversation, streamMessage } from "../api/client";
import type { Message } from "../types";

const CONVERSATION_ID_KEY = "conversationId";

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

  // Load conversation from localStorage on initial render
  useEffect(() => {
    const conversationId = localStorage.getItem(CONVERSATION_ID_KEY);
    if (conversationId === null) return;

    loadConversation(conversationId)
      .then(setMessages)
      .catch(() => localStorage.removeItem(CONVERSATION_ID_KEY));
  }, []);

  function updateLastMessage(updater: (lastMessage: Message) => Message): void {
    setMessages((currentMessages) => [
      ...currentMessages.slice(0, -1),
      updater(currentMessages[currentMessages.length - 1]),
    ]);
  }

  function handleTextDelta(delta: string): void {
    updateLastMessage((lastMessage) => ({
      ...lastMessage,
      content: lastMessage.content + delta,
    }));
  }

  function handleDiagram(code: string): void {
    updateLastMessage((lastMessage) => ({ ...lastMessage, diagram: code }));
  }

  function handleConversationId(conversationId: string): void {
    localStorage.setItem(CONVERSATION_ID_KEY, conversationId);
  }

  async function submitMessage(userInputText: string): Promise<void> {
    setError(null);
    setIsLoading(true);

    const userMessage: Message = { role: "user", content: userInputText };
    const assistantPlaceholder: Message = { role: "assistant", content: "" };
    const messagesWithUser = [...messages, userMessage];
    setMessages([...messagesWithUser, assistantPlaceholder]);

    try {
      await streamMessage(
        {
          messages: messagesWithUser,
          conversation_id: localStorage.getItem(CONVERSATION_ID_KEY),
        },
        handleTextDelta,
        handleDiagram,
        handleConversationId,
      );
    } catch (caughtError) {
      const errorMessage =
        caughtError instanceof Error ? caughtError.message : "Unknown error";
      setError(errorMessage);
      setMessages(messagesWithUser);
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, isLoading, error, submitMessage };
}
