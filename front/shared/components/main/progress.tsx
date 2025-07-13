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
      className={`flex flex-col rounded-xl border shadow-sm border-ui-border overflow-hidden min-h-0 ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        Progress
      </h2>
      <div className="flex flex-col items-center justify-center flex-1 p-4">
        <ProgressCircle progress={progress} size={300} strokeWidth={16} />
        <p className="text-2xl mt-10 mb-4 text-center">You're almost done!</p>
        <TransitionLink
          delay={2000}
          className="underline text-ui-muted text-xl"
          href={`/roadmap/${userId}`}
        >
          Let's continue
        </TransitionLink>
      </div>
    </div>
  );
};
