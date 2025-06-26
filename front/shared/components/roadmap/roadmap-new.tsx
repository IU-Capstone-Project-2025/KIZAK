"use client";

import { useEffect, useRef, useState } from "react";
import { RoadmapNode } from "./node";
import { useRoadmapLayout } from "../../hooks/useRoadmapLayout";
export const rawNodes = [
  {
    node_id: "node-1",
    title: "Introduction",
    summary: "Basics and learning goals",
    progress: 100,
  },
  {
    node_id: "node-2",
    title: "HTML",
    summary: "Page markup and content structure",
    progress: 100,
  },
  {
    node_id: "node-3",
    title: "CSS",
    summary: "Styling and positioning",
    progress: 80,
  },
  {
    node_id: "node-4",
    title: "JavaScript",
    summary: "Fundamentals of logic and interaction",
    progress: 30,
  },
  {
    node_id: "node-5",
    title: "React",
    summary: "Modern approach to UI",
    progress: 0,
  },
];

export const rawLinks = [
  { from_node: "node-1", to_node: "node-2" },
  { from_node: "node-2", to_node: "node-3" },
  { from_node: "node-3", to_node: "node-4" },
  { from_node: "node-4", to_node: "node-5" },
];

export const WORLD_SIZE = 5000;

const SPACING = 30;
const dotRadius = 1;
const dotColor = "#ccc";

interface Props {
  userId: string;
}

export const RoadmapNew: React.FC<Props> = ({ userId }) => {
  const [offset, setOffset] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });
  const [isDragging, setDragging] = useState<boolean>(false);

  const { nodes, measuring, measureElements } = useRoadmapLayout(
    rawNodes,
    rawLinks
  );

  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const lastPos = useRef({ x: 0, y: 0 });

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

  const checkLimit = (obj: { x: number; y: number }) => {
    const container = containerRef.current;
    if (!container) return obj;

    return {
      x: Math.min(0, Math.max(obj.x, container.clientWidth - WORLD_SIZE)),
      y: Math.min(0, Math.max(obj.y, container.clientHeight - WORLD_SIZE)),
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

  const handleOnMouseUp = () => {
    setDragging(false);
  };

  const centerOffset = () => {
    const container = containerRef.current;
    if (!container) return { x: 0, y: 0 };

    return {
      x: container.clientWidth / 2 - WORLD_SIZE / 2,
      y: container.clientHeight / 2 - WORLD_SIZE / 2,
    };
  };

  const moveTo = (targetX: number, targetY: number) => {
    const container = containerRef.current;
    if (!container) return;

    const newOffset = {
      x: container.clientWidth / 2 - targetX,
      y: container.clientHeight / 2 - targetY,
    };

    setOffset(checkLimit(newOffset));
  };

  const animateTo = (targetX: number, targetY: number) => {
    const duration = 600;
    const startTime = performance.now();
    const startOffset = offset;

    const container = containerRef.current;
    if (!container) return;

    const finalOffset = {
      x: container.clientWidth / 2 - targetX,
      y: container.clientHeight / 2 - targetY,
    };

    const easeInOutQuad = (t: number) =>
      t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

    const step = (currentTime: number) => {
      const delta = currentTime - startTime;
      const rawProgress = Math.min(delta / duration, 1);
      const easedProgress = easeInOutQuad(rawProgress);

      const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

      setOffset({
        x: lerp(startOffset.x, finalOffset.x, easedProgress),
        y: lerp(startOffset.y, finalOffset.y, easedProgress),
      });

      if (rawProgress < 1) {
        requestAnimationFrame(step);
      }
    };

    requestAnimationFrame(step);
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

    const center = centerOffset();
    setOffset(center);
  }, [measuring]);

  return (
    <div
      ref={containerRef}
      onMouseDown={(e) => handleOnMouseDown(e)}
      onMouseUp={handleOnMouseUp}
      onMouseMove={(e) => handleOnMouseMove(e)}
      onMouseLeave={handleOnMouseUp}
      className="relative w-full h-full overflow-hidden rounded-b-xl"
    >
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
          id="roadmap"
          width={WORLD_SIZE}
          height={WORLD_SIZE}
          style={{ width: WORLD_SIZE, height: WORLD_SIZE }}
        />
        {measuring && measureElements}
        {!measuring &&
          nodes.map((node) => (
            <div
              key={node.id}
              className="absolute pointer-events-auto"
              style={{
                left: node.x,
                top: node.y,
                width: node.width,
                height: node.height,
              }}
            >
              <RoadmapNode
                onClick={() => animateTo(WORLD_SIZE / 2, WORLD_SIZE / 2)}
                title={node.title}
                description={node.summary}
                progress={
                  node.progress === 100
                    ? "Done"
                    : node.progress === 0
                    ? "Not started"
                    : "In progress"
                }
              />
            </div>
          ))}
        {/* <div
          onClick={() => {
            animateTo(WORLD_SIZE / 2 - 500, WORLD_SIZE / 2 - 500);
          }}
          className="absolute w-50 h-50 bg-amber-300 rounded-xl"
          style={{
            left: WORLD_SIZE / 2 - 100,
            top: WORLD_SIZE / 2 - 100,
          }}
        ></div> */}
      </div>
    </div>
  );
};
