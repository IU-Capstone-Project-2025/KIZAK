"use client";
import { RoadmapNode } from "@/components/node";
import { WORLD_SIZE } from "@/components/roadmap";
import { useEffect, useRef, useState } from "react";

type RawNode = {
  node_id: string;
  title: string;
  summary: string;
  progress: number;
};

type RawLink = {
  from_node: string;
  to_node: string;
};

export type PositionedNode = {
  id: string;
  title: string;
  summary: string;
  progress: number;
  width: number;
  height: number;
  x: number;
  y: number;
  connections: string[];
};

const convertProgress = (progress: number) => {
  if (progress === 100) return "Done";
  if (progress === 0) return "Not started";
  else return "In progress";
};

export const useRoadmapLayout = (rawNodes: RawNode[], rawLinks: RawLink[]) => {
  const [nodes, setNodes] = useState<PositionedNode[]>([]);
  const [measuring, setMeasuring] = useState<boolean>(true);

  const refs = useRef(new Map<string, HTMLDivElement | null>());

  const measureElements = rawNodes.map((el) => (
    <div
      key={el.node_id}
      ref={(rf) => {
        refs.current.set(el.node_id, rf);
      }}
      className="absolute opacity-0"
    >
      <RoadmapNode
        title={el.title}
        description={el.summary}
        progress={convertProgress(el.progress)}
      />
    </div>
  ));

  useEffect(() => {
    let result: PositionedNode[] = [];

    rawNodes.forEach((node) => {
      const rf = refs.current.get(node.node_id);
      if (!rf) return;

      const rect = rf.getBoundingClientRect();
      result.push({
        id: node.node_id,
        title: node.title,
        summary: node.summary,
        progress: node.progress,
        width: rect.width,
        height: rect.height,
        x: 0,
        y: 0,
        connections: rawLinks
          .filter((l) => l.from_node === node.node_id)
          .map((l) => l.to_node),
      });
    });

    const padding = 60;

    const totalWidth =
      result.reduce((acc, node) => acc + node.width, 0) +
      padding * (result.length - 1);

    const startX = WORLD_SIZE / 2 - totalWidth / 2;

    let currentX = startX;
    result.forEach((el) => {
      el.x = currentX;
      el.y = WORLD_SIZE / 2 - el.height / 2;
      currentX += el.width + padding;
    });

    setNodes(result);
    setMeasuring(false);
  }, [rawNodes]);

  return { nodes, measuring, measureElements };
};
