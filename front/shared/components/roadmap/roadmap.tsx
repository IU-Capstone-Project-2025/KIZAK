"use client";
import { useNodePositions } from "@/shared/hooks/useNodePositions";
import { RoadmapNode } from "./node";
import { NodeLink } from "./link";

export const Roadmap = () => {
  const { containerRef, nodesRef, positions } = useNodePositions();
  const keys = Object.keys(positions);

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full overflow-hidden p-4"
    >
      <div className="absolute inset-0">
        <div className="relative flex-center transition-all duration-200 gap-x-22 w-full h-full">
          <RoadmapNode
            ref={(el) => {
              nodesRef.current["node-1"] = el;
            }}
            title={"Basics of programming"}
            description={"Html, Css, JavaScript basics"}
            progress={"Done"}
          />

          <RoadmapNode
            ref={(el) => {
              nodesRef.current["node-2"] = el;
            }}
            title={"React development"}
            description={"Hooks, Render, Typescript"}
            progress={"In progress"}
          />

          <RoadmapNode
            ref={(el) => {
              nodesRef.current["node-3"] = el;
            }}
            title={"Backend development"}
            description={"Node.js, Databases"}
            progress={"Not started"}
          />

          {/* Линки */}
          {keys.length > 1 &&
            keys.slice(0, -1).map((_, i) => {
              const node1 = keys[i];
              const node2 = keys[i + 1];
              if (!positions[node1] || !positions[node2]) return null;
              return (
                <NodeLink
                  key={i}
                  from={{
                    x: positions[node1].xRight,
                    y: positions[node1].y,
                  }}
                  to={{
                    x: positions[node2].xLeft,
                    y: positions[node2].y,
                  }}
                />
              );
            })}
        </div>
      </div>
    </div>
  );
};
