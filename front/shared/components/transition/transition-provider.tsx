"use client";
import { useRouter } from "next/navigation";
import React, { createContext, useContext, useState } from "react";
import { ANIMATION_TIME } from ".";

interface TransitionContextType {
  handleClick: (href: string, delay: number) => void;
  isTransitioning: boolean;
}

const TransitionContext = createContext<TransitionContextType>({
  handleClick: () => {},
  isTransitioning: false,
});

export const TransitionProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [isTransitioning, setTransitioning] = useState<boolean>(false);
  const router = useRouter();

  const start = () => setTransitioning(true);
  const end = () => setTransitioning(false);

  const handleClick = (href: string, delay: number = 0) => {
    start();
    setTimeout(() => {
      router.push(href);
      setTimeout(() => {
        end();
      }, delay);
    }, ANIMATION_TIME);
  };

  return (
    <TransitionContext.Provider value={{ handleClick, isTransitioning }}>
      {children}
    </TransitionContext.Provider>
  );
};

export const usePageTransition = () => useContext(TransitionContext);
