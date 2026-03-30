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
  const [conversationId, setConversationId] = useState<string | null>(
    localStorage.getItem(CONVERSATION_ID_KEY),
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const storedConversationId = localStorage.getItem(CONVERSATION_ID_KEY);
    if (storedConversationId === null) return;

    loadConversation(storedConversationId)
      .then(setMessages)
      .catch(() => {
        localStorage.removeItem(CONVERSATION_ID_KEY);
        setConversationId(null);
      });
  }, []);

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

    function onConversationId(newConversationId: string): void {
      setConversationId(newConversationId);
      localStorage.setItem(CONVERSATION_ID_KEY, newConversationId);
    }

    try {
      await streamMessage({ messages: messagesWithUser, conversation_id: conversationId }, onTextDelta, onDiagram, onConversationId);
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
