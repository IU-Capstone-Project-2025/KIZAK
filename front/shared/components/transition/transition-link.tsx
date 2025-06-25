"use client";
import { useRouter } from "next/navigation";
import React from "react";
import { usePageTransition } from "./transition-provider";

interface TransitionLinkProps {
  href: string;
  className?: string;
}

export const TransitionLink: React.FC<
  React.PropsWithChildren<TransitionLinkProps>
> = ({ href, className, children }) => {
  const router = useRouter();
  const { handleClick } = usePageTransition();

  return (
    <button
      onMouseEnter={() => router.prefetch(href)}
      onClick={() => handleClick(href)}
      className={`cursor-pointer ${className}`}
    >
      {children}
    </button>
  );
};
