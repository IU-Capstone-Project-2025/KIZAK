"use client";
import { useEffect, useRef, useState, useMemo } from "react";
import { RoadmapNode } from "../components/roadmap/node";

export type RawNode = {
  node_id: string;
  title: string;
  summary: string;
  resource_id: string;
};

type RawLink = {
  from_node: string;
  to_node: string;
};

export type Progress = "Done" | "In progress" | "Not started";

export type PositionedNode = {
  id: string;
  title: string;
  summary: string;
  width: number;
  height: number;
  x: number;
  y: number;
  connections: string[];
};

export const useRoadmapLayout = (rawNodes: RawNode[], rawLinks: RawLink[]) => {
  const [nodes, setNodes] = useState<PositionedNode[]>([]);
  const [measuring, setMeasuring] = useState<boolean>(true);
  const [worldWidth, setWorldWidth] = useState<number>(3000);

  const refs = useRef(new Map<string, HTMLDivElement | null>());

  const measureElements = useMemo(() => {
    return rawNodes.map((el) => (
      <div
        key={el.node_id}
        ref={(rf) => {
          refs.current.set(el.node_id, rf);
        }}
        className="absolute opacity-0 pointer-events-none select-none"
        style={{ userSelect: "none" }}
      >
        <RoadmapNode
          title={el.title}
          description={el.summary}
          progress="Not started"
        />
      </div>
    ));
  }, [rawNodes]);

  useEffect(() => {
    if (rawNodes.length === 0) return;

    let result: PositionedNode[] = [];

    rawNodes.forEach((node) => {
      const rf = refs.current.get(node.node_id);
      if (!rf) return;

      const rect = rf.getBoundingClientRect();
      result.push({
        id: node.node_id,
        title: node.title,
        summary: node.summary,
        width: rect.width,
        height: rect.height,
        x: 0,
        y: 0,
        connections: rawLinks
          .filter((l) => l.from_node === node.node_id)
          .map((l) => l.to_node),
      });
    });

    if (result.length === 0) return;

    const padding = 60;
    const leftRightPadding = 500;

    const totalWidth =
      result.reduce((acc, node) => acc + node.width, 0) +
      padding * (result.length - 1);

    const worldWidthCalculated = totalWidth + 2 * leftRightPadding;
    setWorldWidth(worldWidthCalculated);

    const startX = leftRightPadding;

    let currentX = startX;
    result.forEach((el) => {
      el.x = currentX;
      el.y = 2500 / 2 - el.height / 2;
      currentX += el.width + padding;
    });

    setNodes(result);
    setMeasuring(false);
  }, [rawNodes, rawLinks]);

  return { nodes, measuring, measureElements, worldWidth };
};
