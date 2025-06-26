"use client";
import { useRef, useEffect, useState } from "react";

interface Position {
  xLeft: number;
  xRight: number;
  y: number;
}

export function useNodePositions() {
  const [positions, setPositions] = useState<Record<string, Position>>({});
  const nodesRef = useRef<Record<string, HTMLDivElement | null>>({});
  const containerRef = useRef<HTMLDivElement | null>(null);

  const animationFrameRef = useRef<number | null>(null);

  const updatePositions = () => {
    const containerRect = containerRef.current?.getBoundingClientRect();
    if (!containerRect) return;

    const newPositions: Record<string, Position> = {};
    let changed = false;

    Object.entries(nodesRef.current).forEach(([id, el]) => {
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const pos = {
        xLeft: rect.left - containerRect.left,
        xRight: rect.right - containerRect.left,
        y: rect.top - containerRect.top + Math.floor(rect.height / 2),
      };

      if (
        !positions[id] ||
        pos.xLeft !== positions[id].xLeft ||
        pos.xRight !== positions[id].xRight ||
        pos.y !== positions[id].y
      ) {
        changed = true;
        newPositions[id] = pos;
      } else {
        newPositions[id] = positions[id];
      }
    });

    if (changed) {
      setPositions(newPositions);
    }

    animationFrameRef.current = requestAnimationFrame(updatePositions);
  };

  useEffect(() => {
    animationFrameRef.current = requestAnimationFrame(updatePositions);
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  return { containerRef, nodesRef, positions };
}
