"use client";
import React from "react";
import { usePageTransition } from "./transition-provider";
import { useRouter } from "next/navigation";

interface TransitionLinkProps {
  href: string;
  delay?: number;
  className?: string;
}

export const TransitionLink: React.FC<
  React.PropsWithChildren<TransitionLinkProps>
> = ({ href, delay = 0, className, children }) => {
  const router = useRouter();
  const { handleClick } = usePageTransition();

  return (
    <button
      onMouseEnter={() => router.prefetch(href)}
      onClick={() => handleClick(href, delay)}
      className={`cursor-pointer ${className}`}
    >
      {children}
    </button>
  );
};
