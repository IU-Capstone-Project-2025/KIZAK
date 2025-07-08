"use client";

import { useEffect, useRef, useState } from "react";
import { RoadmapNode } from "./node";
import { useRoadmapLayout } from "../../hooks/useRoadmapLayout";
import Link from "next/link";

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
  initialNodeId?: string;
}

export const RoadmapNew: React.FC<Props> = ({ userId, initialNodeId }) => {
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setDragging] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(
    initialNodeId || null
  );

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

  const checkLimit = (pos: { x: number; y: number }) => {
    const container = containerRef.current;
    if (!container) return pos;
    const halfWidth = container.clientWidth / 2;
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
    setSelectedNode(nodeId);

    // 👇 Меняем адрес без перезагрузки
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

    // 👇 Удаляем nodeId из адреса
    window.history.pushState(null, "", `/roadmap/${userId}`);
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

  // 🎯 Анимация при открытии по initialNodeId
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
          <div
            className="relative flex flex-col h-full p-6 rounded-md shadow-md overflow-auto
               bg-bg-main text-ui-dark border border-ui-border"
          >
            <button
              onClick={handleClose}
              aria-label="Close"
              className="absolute top-4 right-4 w-8 h-8 flex-center rounded-full
                 text-ui-muted hover:text-ui-dark
                 cursor-pointer
                 transition-colors duration-200 ease-in-out"
              title="Закрыть"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-5 h-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>

            <h3 className="text-3xl font-extrabold mb-4 text-brand-primary">
              Python OOP
            </h3>
            <p className="mb-4 text-lg leading-relaxed">
              Basics of OOP for Python
            </p>

            <Link
              href="https://stepik.org/course/98974/promo?search=7287873917"
              target="_blank"
              rel="noopener noreferrer"
              className="mb-6 text-brand-primary underline hover:text-yellow-400 transition"
            >
              Перейти к курсу
            </Link>

            <div className="grid grid-cols-2 gap-x-12 gap-y-4 text-ui-dark text-sm font-semibold">
              <div className="flex-between">
                <span className="text-ui-muted">Уровень:</span>
                <span>Beginner</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Цена:</span>
                <span>Бесплатно</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Язык:</span>
                <span>Russian</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Длительность:</span>
                <span>10 часов</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Платформа:</span>
                <span>KIZAK</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Рейтинг:</span>
                <span>0</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Дата публикации:</span>
                <span>2015-05-01</span>
              </div>
              <div className="flex-between">
                <span className="text-ui-muted">Сертификат:</span>
                <span className="text-status-success">Доступен</span>
              </div>
              <div className="col-span-2 mt-4">
                <span className="text-ui-muted font-semibold">
                  Навыки, изучаемые:
                </span>
                <div className="mt-1 flex flex-wrap gap-2">
                  <span className="px-2 py-1 rounded shadow-sm font-medium border border-ui-border text-ui-dark">
                    Python
                  </span>
                  <span className="px-2 py-1 rounded shadow-sm font-medium border border-ui-border text-ui-dark">
                    OOP
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
