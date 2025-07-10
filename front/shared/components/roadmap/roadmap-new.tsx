"use client";

import { useEffect, useRef, useState } from "react";
import { RoadmapNode } from "./node";
import {
  RawNode,
  useRoadmapLayout,
  Progress,
  PositionedNode,
} from "../../hooks/useRoadmapLayout";
import Link from "next/link";
import { CustomSelect } from "./select";
import { fetchRoadmapData } from "@/shared/utils/roadmapConverter";
import { RawLink } from "@/shared/types/types";
import { ResourceDetails } from "./resource-details";

export const WORLD_SIZE = 5000;
const SPACING = 30;
const dotRadius = 1;
const dotColor = "#ccc";

interface Props {
  userId: string;
  initialNodeId?: string;
}

export const RoadmapNew: React.FC<Props> = ({ userId, initialNodeId }) => {
  const [rawNodes, setRawNodes] = useState<RawNode[]>([]);
  const [rawLinks, setRawLinks] = useState<RawLink[]>([]);
  const [initialProgress, setInitialProgress] = useState<
    Record<string, Progress>
  >({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [progressMap, setProgressMap] = useState<Record<string, Progress>>({});
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setDragging] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(
    initialNodeId || null
  );
  const [roadmapId, setRoadmapId] = useState<string>("");

  const { nodes, measuring, measureElements } = useRoadmapLayout(
    rawNodes,
    rawLinks
  );
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const lastPos = useRef({ x: 0, y: 0 });
  const [prevOffsetBeforeSelection, setPrevOffsetBeforeSelection] = useState<{
    x: number;
    y: number;
  } | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchRoadmapData(userId);
        setRawNodes(data.rawNodes);
        setRawLinks(data.rawLinks);
        setInitialProgress(data.initialProgress);
        setProgressMap(data.initialProgress);
        setRoadmapId(data.roadmapId);
      } catch (err) {
        setError("Failed to load roadmap data");
        console.error("Error loading roadmap data:", err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [userId]);

  const drawDots = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, WORLD_SIZE, WORLD_SIZE);
    ctx.fillStyle = dotColor;
    for (let x = 0; x < WORLD_SIZE; x += SPACING) {
      for (let y = 0; y < WORLD_SIZE; y += SPACING) {
        ctx.beginPath();
        ctx.arc(x, y, dotRadius, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  };

  const checkLimit = (pos: { x: number; y: number }) => {
    const container = containerRef.current;
    if (!container) return pos;
    const halfWidth = container.clientWidth;
    return {
      x: Math.min(0, Math.max(pos.x, halfWidth - WORLD_SIZE)),
      y: Math.min(0, Math.max(pos.y, container.clientHeight - WORLD_SIZE)),
    };
  };

  const handleOnMouseDown = (e: React.MouseEvent) => {
    setDragging(true);
    lastPos.current = { x: e.clientX, y: e.clientY };
  };

  const handleOnMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    const dx = e.clientX - lastPos.current.x;
    const dy = e.clientY - lastPos.current.y;
    setOffset((prev) => checkLimit({ x: prev.x + dx, y: prev.y + dy }));
    lastPos.current = { x: e.clientX, y: e.clientY };
  };

  const handleOnMouseUp = () => setDragging(false);

  const animateTo = (targetX: number, targetY: number) => {
    const duration = 600;
    const startTime = performance.now();
    const startOffset = offset;
    const container = containerRef.current;
    if (!container) return;

    const easeInOutQuad = (t: number) =>
      t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

    const step = (currentTime: number) => {
      const delta = currentTime - startTime;
      const progress = Math.min(delta / duration, 1);
      const eased = easeInOutQuad(progress);
      setOffset({
        x: lerp(startOffset.x, targetX, eased),
        y: lerp(startOffset.y, targetY, eased),
      });
      if (progress < 1) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  };

  const handleOnNodeClick = (nodeId: string) => {
    setPrevOffsetBeforeSelection(offset);
    setSelectedNode(nodeId);

    window.history.pushState(null, "", `/roadmap/${userId}/${nodeId}`);

    const container = containerRef.current;
    const node = nodes.find((n) => n.id === nodeId);
    if (!container || !node) return;

    const halfWidth = container.clientWidth / 2;
    const centerX = node.x + node.width / 2;
    const centerY = node.y + node.height / 2;
    const targetX = halfWidth / 2 - centerX;
    const targetY = container.clientHeight / 2 - centerY;

    animateTo(targetX, targetY);
  };

  const handleClose = () => {
    setSelectedNode(null);
    window.history.pushState(null, "", `/roadmap/${userId}`);
    if (prevOffsetBeforeSelection) {
      animateTo(prevOffsetBeforeSelection.x, prevOffsetBeforeSelection.y);
      setPrevOffsetBeforeSelection(null);
    }
  };

  const drawLinks = () => {
    const canvas = canvasRef.current;
    if (!canvas || measuring) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, WORLD_SIZE, WORLD_SIZE);
    drawDots();
    ctx.strokeStyle = "#ccc";
    ctx.lineWidth = 1.2;
    nodes.forEach((node) => {
      node.connections.forEach((targetId) => {
        const target = nodes.find((n) => n.id === targetId);
        if (!target) return;
        const fromX = node.x + node.width / 2;
        const fromY = node.y + node.height / 2;
        const toX = target.x + target.width / 2;
        const toY = target.y + target.height / 2;
        ctx.beginPath();
        ctx.moveTo(fromX, fromY);
        ctx.lineTo(toX, toY);
        ctx.stroke();
      });
    });
  };

  const handleProgressChange = async (
    nodeId: string,
    newProgress: Progress
  ) => {
    setProgressMap((prev) => ({ ...prev, [nodeId]: newProgress }));

    try {
      await fetch("http://localhost:8000/node/", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          node_id: nodeId,
          progress: newProgress,
        }),
      });
      console.log("Progress updated");
    } catch (err) {
      console.error("Failed to update progress", err);
    }
  };

  const selectedNodeData: PositionedNode | null = selectedNode
    ? nodes.find((n) => n.id === selectedNode) ?? null
    : null;

  const selectedRawNode = selectedNode
    ? rawNodes.find((n) => n.node_id === selectedNode) ?? null
    : null;

  const selectedResourceId = selectedRawNode?.resource_id ?? null;

  const selectedNodeProgress: Progress = selectedNode
    ? progressMap[selectedNode]
    : "Not started";

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = WORLD_SIZE * dpr;
    canvas.height = WORLD_SIZE * dpr;
    canvas.style.width = `${WORLD_SIZE}px`;
    canvas.style.height = `${WORLD_SIZE}px`;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);

    drawDots();
    drawLinks();
  }, [measuring, selectedNode, nodes]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const center = {
      x: container.clientWidth / 2 / 2 - WORLD_SIZE / 2,
      y: container.clientHeight / 2 - WORLD_SIZE / 2,
    };
    setOffset(checkLimit(center));
  }, []);

  useEffect(() => {
    if (!initialNodeId || measuring) return;

    const node = nodes.find((n) => n.id === initialNodeId);
    const container = containerRef.current;
    if (!node || !container) return;

    const halfWidth = container.clientWidth / 2;
    const centerX = node.x + node.width / 2;
    const centerY = node.y + node.height / 2;
    const targetX = halfWidth / 2 - centerX;
    const targetY = container.clientHeight / 2 - centerY;

    animateTo(targetX, targetY);
    setSelectedNode(initialNodeId);
  }, [initialNodeId, measuring, nodes]);

  return (
    <div
      ref={containerRef}
      onMouseDown={handleOnMouseDown}
      onMouseUp={handleOnMouseUp}
      onMouseMove={handleOnMouseMove}
      onMouseLeave={handleOnMouseUp}
      className="relative w-full h-full overflow-hidden rounded-b-xl flex"
      style={{ userSelect: isDragging ? "none" : "auto" }}
    >
      <div className="relative h-full overflow-hidden w-full">
        <div
          className="absolute origin-center"
          style={{
            width: WORLD_SIZE,
            height: WORLD_SIZE,
            transform: `translate(${offset.x}px, ${offset.y}px)`,
          }}
        >
          <canvas
            ref={canvasRef}
            width={WORLD_SIZE}
            height={WORLD_SIZE}
            style={{ width: WORLD_SIZE, height: WORLD_SIZE }}
          />
          {measuring && measureElements}
          {!measuring &&
            nodes.map((node) => (
              <div
                key={node.id}
                className="absolute cursor-pointer"
                style={{
                  left: node.x,
                  top: node.y,
                  width: node.width,
                  height: node.height,
                }}
                onClick={() => handleOnNodeClick(node.id)}
              >
                <RoadmapNode
                  title={node.title}
                  description={node.summary}
                  progress={progressMap[node.id] || "Not started"}
                />
              </div>
            ))}
        </div>
      </div>

      <div
        className={`
    absolute top-0 right-0 h-full w-1/2 bg-none p-6 overflow-auto z-10
    transition-all duration-300
    ${
      selectedNode
        ? "opacity-100 visible pointer-events-auto"
        : "opacity-0 invisible pointer-events-none"
    }
  `}
      >
        <div className="w-full h-full">
          {selectedNode && (
            <ResourceDetails
              resourceId={selectedResourceId ?? ""}
              onClose={handleClose}
              progress={selectedNodeProgress}
              onProgressChange={(val) =>
                handleProgressChange(selectedNode, val as Progress)
              }
              node_id={selectedNode}
              roadmap_id={roadmapId}
              user_id={userId}
            />
          )}
        </div>
      </div>
    </div>
  );
};
