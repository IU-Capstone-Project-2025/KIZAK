"use client";
import React, { useEffect, useState } from "react";
import { usePageTransition } from "./transition-provider";
import Image from "next/image";
import { ANIMATION_TIME } from ".";

export const TransitionOverlay = () => {
  const { isTransitioning } = usePageTransition();
  const [spin, setSpin] = useState(false);

  useEffect(() => {
    if (isTransitioning) {
      const timeout = setTimeout(() => setSpin(true), ANIMATION_TIME);
      return () => {
        clearTimeout(timeout);
        setSpin(false);
      };
    } else {
      setSpin(false);
    }
  }, [isTransitioning]);

  return (
    <div
      className={`fixed inset-0 z-50 bg-bg-main flex-center transition-all duration-${ANIMATION_TIME} ${
        isTransitioning ? "opacity-100 visible" : "opacity-0 invisible"
      }`}
    >
      <Image
        className={`transition-all duration-${ANIMATION_TIME} ${
          isTransitioning
            ? spin
              ? "animate-logo-spin-scale"
              : "scale-105"
            : "scale-90"
        }`}
        priority
        width={80}
        height={80}
        src="/logo.svg"
        alt="KIZAK"
      />
    </div>
  );
};
