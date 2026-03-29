import { useDiagram } from "../../hooks/useDiagram";

interface MermaidDiagramProps {
  diagramCode: string | null;
}

export function MermaidDiagram({ diagramCode }: MermaidDiagramProps) {
  const containerRef = useDiagram(diagramCode);

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
