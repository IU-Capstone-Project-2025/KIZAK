"use client";
import { useRouter } from "next/navigation";
import React, { createContext, useContext, useState } from "react";
import { ANIMATION_TIME } from ".";

const TransitionContext = createContext<{
  handleClick: (href: string) => void;
  isTransitioning: boolean;
}>({
  handleClick: () => {},
  isTransitioning: false,
});

export const TransitionProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [isTransitioning, setTransitioning] = useState<boolean>(false);
  const router = useRouter();

  const start = () => {
    setTransitioning(true);
  };
  const end = () => {
    setTransitioning(false);
  };
  const handleClick = (href: string) => {
    start();

    setTimeout(() => {
      router.push(href);
      setTimeout(() => {
        end();
      }, ANIMATION_TIME);
    }, ANIMATION_TIME);
  };
  return (
    <TransitionContext
      value={{ handleClick: handleClick, isTransitioning: isTransitioning }}
    >
      {children}
    </TransitionContext>
  );
};

export const usePageTransition = () => useContext(TransitionContext);
