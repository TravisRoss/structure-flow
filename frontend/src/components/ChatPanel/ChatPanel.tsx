import { MessageForm } from "./MessageForm";
import { MessageList } from "./MessageList";
import type { UseChat } from "../../hooks/useChat";

interface ChatPanelProps {
  chatState: UseChat;
}

export function ChatPanel({ chatState: { messages, isLoading, error, submitMessage } }: ChatPanelProps) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        borderRight: "1px solid #ddd",
      }}
    >
      <MessageList messages={messages} isLoading={isLoading} />

      {error && (
        <div
          style={{
            padding: "0.75rem 1rem",
            backgroundColor: "#ffe6e6",
            color: "#d32f2f",
            borderTop: "1px solid #ddd",
            fontSize: "0.875rem",
          }}
        >
          {error}
        </div>
      )}

      <div style={{ padding: "1rem", borderTop: "1px solid #ddd" }}>
        <MessageForm isLoading={isLoading} onSubmit={submitMessage} />
      </div>
    </div>
  );
}
