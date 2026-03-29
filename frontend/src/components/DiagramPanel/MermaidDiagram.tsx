import { useDiagram } from "../../hooks/useDiagram";

interface MermaidDiagramProps {
  diagramCode: string | null;
}

export function MermaidDiagram({ diagramCode }: MermaidDiagramProps) {
  const containerRef = useDiagram(diagramCode);

  if (!diagramCode) {
    return (
      <div style={{ width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center", color: "#999" }}>
        Your diagram will appear here
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height: "100%",
        overflow: "auto",
        padding: "1rem",
      }}
    />
  );
}
