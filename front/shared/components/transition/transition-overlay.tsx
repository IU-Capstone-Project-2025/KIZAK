"use client";
import React from "react";
import { usePageTransition } from "./transition-provider";
import Image from "next/image";
import { ANIMATION_TIME } from ".";

export const TransitionOverlay = () => {
  const { isTransitioning } = usePageTransition();

  return (
    <div
      className={`fixed top-0 left-0 right-0 bottom-0 z-50 bg-bg-main flex-center transition-all duration-${ANIMATION_TIME} ${
        isTransitioning ? "opacity-100 visible" : "opacity-0 invisible"
      }`}
    >
      <Image
        className={`transition-all duration-${ANIMATION_TIME} ${
          isTransitioning ? "scale-105" : "scale-90"
        }`}
        priority={true}
        width={80}
        height={80}
        src={"/logo.svg"}
        alt={"KIZAK"}
      />
    </div>
  );
};
