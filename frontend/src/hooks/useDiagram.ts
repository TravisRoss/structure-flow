import { useEffect, useRef } from "react";
import mermaid from "mermaid";

export function useDiagram(diagramCode: string | null) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!diagramCode) return;

    const container = containerRef.current;
    if (!container) return;

    const renderDiagram = async () => {
      try {
        container.innerHTML = "";
        const renderResult = await mermaid.render("diagram", diagramCode);
        container.innerHTML = renderResult.svg;
      } catch (error) {
        container.innerHTML = `<p style="color: red;">Error rendering diagram: ${error instanceof Error ? error.message : "Unknown error"}</p>`;
      }
    };

    renderDiagram();
  }, [diagramCode]);

  return containerRef;
}
