"use client";
import { useLayoutEffect, useRef, useState } from "react";

interface Position {
  xLeft: number;
  xRight: number;
  y: number;
}

export function useNodePositions() {
  const [positions, setPositions] = useState<Record<string, Position>>({});
  const nodesRef = useRef<Record<string, HTMLDivElement | null>>({});
  const containerRef = useRef<HTMLDivElement | null>(null);

  const updatePositions = () => {
    const containerRect = containerRef.current?.getBoundingClientRect();
    if (!containerRect) return;

    const newPositions: Record<string, Position> = {};
    Object.entries(nodesRef.current).forEach(([id, el]) => {
      if (!el) return;
      const rect = el.getBoundingClientRect();
      newPositions[id] = {
        xLeft: rect.left - containerRect.left,
        xRight: rect.right - containerRect.left,
        y: rect.top - containerRect.top + Math.floor(rect.height / 2),
      };
    });

    setPositions(newPositions);
  };

  useLayoutEffect(() => {
    updatePositions();
    window.addEventListener("resize", updatePositions);
    window.addEventListener("scroll", updatePositions, true);
    return () => {
      window.removeEventListener("resize", updatePositions);
      window.removeEventListener("scroll", updatePositions, true);
    };
  }, []);

  return { containerRef, nodesRef, positions, updatePositions };
}
