import { useChat } from "./hooks/useChat";
import { ChatPanel } from "./components/ChatPanel/ChatPanel";
import { MermaidDiagram } from "./components/DiagramPanel/MermaidDiagram";

function App() {
  const chatState = useChat();
  const lastMessage = chatState.messages.findLast((message) => message.diagram != null);
  const currentDiagram = lastMessage?.diagram ?? null;

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ width: "25%" }}>
        <ChatPanel chatState={chatState} />
      </div>
      <div style={{ width: "75%" }}>
        <MermaidDiagram diagramCode={currentDiagram} />
      </div>
    </div>
  );
}

export default App;
