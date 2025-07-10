import React from "react";
import { ProgressCircle } from "../progress-circle";
import { TransitionLink } from "../transition/transition-link";

interface Props {
  className?: string;
  userId?: string;
  progress: number;
}

export const MainProgress: React.FC<Props> = ({
  className = "",
  userId,
  progress,
}) => {
  return (
    <div
      className={`flex flex-col rounded-xl border shadow-sm border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-sm w-full pl-2 py-0.5 border-b border-ui-border">
        Progress
      </h2>
      <div className="flex flex-col items-center justify-center flex-1 p-0.5 overflow-auto">
        <ProgressCircle progress={progress} size={220} strokeWidth={6} />
        <p className="text-base mt-1 mb-0.5 text-center">You're almost done!</p>
        <TransitionLink
          delay={2000}
          className="underline text-ui-muted text-sm"
          href={`/roadmap/${userId}`}
        >
          Let's continue
        </TransitionLink>
      </div>
    </div>
  );
};
