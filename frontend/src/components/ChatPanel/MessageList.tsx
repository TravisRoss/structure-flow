import { useEffect, useRef } from "react";

import type { Message } from "../../types";

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
      }}
    >
      {messages.length === 0 && (
        <div style={{ color: "#999", textAlign: "center" }}>
          Start a conversation...
        </div>
      )}
      {messages.map((message, index) => (
        <div
          key={index}
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "0.5rem",
            padding: "0.75rem",
            borderRadius: "4px",
            backgroundColor: message.role === "user" ? "#e7f3ff" : "#f0f0f0",
          }}
        >
          <strong style={{ fontSize: "0.875rem", color: "#666" }}>
            {message.role === "user" ? "You" : "Assistant"}
          </strong>
          <p style={{ margin: 0, wordBreak: "break-word" }}>
            {message.content}
          </p>
        </div>
      ))}
      {isLoading && (
        <div
          style={{
            padding: "0.75rem",
            borderRadius: "4px",
            backgroundColor: "#f0f0f0",
            color: "#999",
            fontSize: "0.875rem",
          }}
        >
          Thinking...
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
