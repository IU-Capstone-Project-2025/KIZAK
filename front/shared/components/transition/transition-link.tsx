"use client";
import React from "react";
import { usePageTransition } from "./transition-provider";
import { useRouter } from "next/navigation";

interface TransitionLinkProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  href: string;
  delay?: number;
  className?: string;
}

export const TransitionLink: React.FC<
  React.PropsWithChildren<TransitionLinkProps>
> = ({ href, delay = 0, className, children, ...rest }) => {
  const router = useRouter();
  const { handleClick } = usePageTransition();

  return (
    <button
      {...rest}
      onMouseEnter={(e) => {
        router.prefetch(href);
        rest.onMouseEnter?.(e);
      }}
      onClick={(e) => {
        handleClick(href, delay);
        rest.onClick?.(e);
      }}
      className={`cursor-pointer ${className}`}
    >
      {children}
    </button>
  );
};
