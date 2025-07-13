"use client";

import React, { useEffect, useState } from "react";
import { useNodePositions } from "@/shared/hooks/useNodePositions";
import { RoadmapNode } from "./node";
import { NodeLink } from "./link";
import { fetchRoadmapData } from "@/shared/utils/roadmapConverter";
import { RawNode, RawLink, Progress } from "@/shared/types/types";

interface Props {
  userId: string;
}

export const RoadmapMiniPreview: React.FC<Props> = ({ userId }) => {
  const { containerRef, nodesRef, positions } = useNodePositions();
  const keys = Object.keys(positions);
  
  const [roadmapData, setRoadmapData] = useState<{
    rawNodes: RawNode[];
    rawLinks: RawLink[];
    initialProgress: Record<string, Progress>;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadRoadmapData = async () => {
      try {
        setLoading(true);
        const data = await fetchRoadmapData(userId);
        setRoadmapData(data);
      } catch (err) {
        setError("Failed to load roadmap data");
        console.error("Error loading roadmap data:", err);
      } finally {
        setLoading(false);
      }
    };

    loadRoadmapData();
  }, [userId]);

  if (loading) {
    return (
      <div className="absolute w-full h-full p-4 flex items-center justify-center">
        <div className="flex flex-col items-center gap-2">
          <div className="w-4 h-4 border-2 border-ui-border border-t-ui-dark rounded-full animate-spin"></div>
          <div className="text-ui-dark text-sm">Loading roadmap...</div>
        </div>
      </div>
    );
  }

  if (error || !roadmapData) {
    return (
      <div className="absolute w-full h-full p-4 flex items-center justify-center">
        <div className="text-ui-dark text-sm">Failed to load roadmap</div>
      </div>
    );
  }

  // Показываем только первые 3 узла для превью
  const previewNodes = roadmapData.rawNodes.slice(0, 3);

  // Если нет узлов, показываем сообщение
  if (previewNodes.length === 0) {
    return (
      <div className="absolute w-full h-full p-4 flex items-center justify-center">
        <div className="text-ui-dark text-sm">No roadmap nodes found</div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="absolute w-full h-full p-4 flex items-center justify-center"
    >
      {previewNodes.map((node, index) => (
        <React.Fragment key={node.node_id}>
          <RoadmapNode
            ref={(el) => {
              nodesRef.current[`node-${index + 1}`] = el;
            }}
            title={node.title}
            description={node.summary}
            progress={roadmapData.initialProgress[node.node_id] || "Not started"}
          />
          
          {index < previewNodes.length - 1 && <div className="w-50" />}
        </React.Fragment>
      ))}

      {/* Линки между узлами */}
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
