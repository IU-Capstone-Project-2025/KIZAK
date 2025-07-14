import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";

export const Portal = ({ children }: { children: React.ReactNode }) => {
  const elRef = useRef<HTMLDivElement | null>(null);
  if (!elRef.current) {
    elRef.current = document.createElement("div");
  }

  useEffect(() => {
    const portalRoot = document.body;
    portalRoot.appendChild(elRef.current!);
    return () => {
      portalRoot.removeChild(elRef.current!);
    };
  }, []);

  return createPortal(children, elRef.current);
}; 
