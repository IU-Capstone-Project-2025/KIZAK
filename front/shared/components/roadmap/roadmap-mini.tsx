"use client";
import { useNodePositions } from "@/shared/hooks/useNodePositions";
import { RoadmapNode } from "./node";
import { NodeLink } from "./link";

/*
    Here will be only 3 close nodes from main roadmap
*/
export const RoadmapMini = () => {
  const { containerRef, nodesRef, positions } = useNodePositions();
  const keys = Object.keys(positions);

  return (
    <div
      ref={containerRef}
      className="absolute w-full h-full p-4 flex items-center justify-center"
    >
      <RoadmapNode
        ref={(el) => {
          nodesRef.current["node-1"] = el;
        }}
        title={"Basics of programming"}
        description={"Html, Css, JavaScript basics"}
        progress={"Done"}
      />

      <div className="w-50" />

      <RoadmapNode
        ref={(el) => {
          nodesRef.current["node-2"] = el;
        }}
        title={"React development"}
        description={"Hooks, Render, Typescript"}
        progress={"In progress"}
      />

      <div className="w-50" />

      <RoadmapNode
        ref={(el) => {
          nodesRef.current["node-3"] = el;
        }}
        title={"Basics of programming"}
        description={"Html, Css, JavaScript basics"}
        progress={"Not started"}
      />

      {keys.length > 1 &&
        keys.slice(0, -1).map((_, i) => {
          const node1 = keys[i];
          const node2 = keys[i + 1];
          if (!positions[node1] || !positions[node2]) return null;
          return (
            <NodeLink
              key={i}
              from={{ x: positions[node1].xRight, y: positions[node1].y }}
              to={{ x: positions[node2].xLeft, y: positions[node2].y }}
            />
          );
        })}
    </div>
  );
};
