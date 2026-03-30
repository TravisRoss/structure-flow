export type Role = "user" | "assistant";

export interface Message {
  role: Role;
  content: string;
  diagram?: string | null;
}

export interface ChatRequest {
  messages: Message[];
  conversation_id: string | null;
}

export interface ChatResponse {
  message: string;
  diagram: string | null;
}
