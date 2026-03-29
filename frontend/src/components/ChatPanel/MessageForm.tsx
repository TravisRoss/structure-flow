import { useState } from "react";

interface MessageFormProps {
  isLoading: boolean;
  onSubmit: (message: string) => void;
}

export function MessageForm({ isLoading, onSubmit }: MessageFormProps) {
  const [inputValue, setInputValue] = useState("");

  const handleSubmit = (event: React.SyntheticEvent<HTMLFormElement>): void => {
    event.preventDefault();
    if (!inputValue.trim()) return;

    onSubmit(inputValue);
    setInputValue("");
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", gap: "0.5rem" }}>
      <input
        type="text"
        value={inputValue}
        onChange={(event) => setInputValue(event.currentTarget.value)}
        placeholder="Type your message..."
        disabled={isLoading}
        style={{
          flex: 1,
          padding: "0.75rem",
          border: "1px solid #ddd",
          borderRadius: "4px",
          fontSize: "1rem",
        }}
      />
      <button
        type="submit"
        disabled={isLoading}
        style={{
          padding: "0.75rem 1.5rem",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: isLoading ? "not-allowed" : "pointer",
          opacity: isLoading ? 0.6 : 1,
        }}
      >
        {isLoading ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
