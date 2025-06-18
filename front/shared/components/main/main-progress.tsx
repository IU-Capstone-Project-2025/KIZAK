import React from "react";
import { ProgressCircle } from "../progress-circle";

interface Props {
  className?: string;
}

export const MainProgress: React.FC<Props> = ({ className = "" }) => {
  return (
    <div
      className={`w-1/3 h-full rounded-xl border border-ui-border flex flex-col ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        Progress
      </h2>
      <div className="flex-center flex-col gap-y-12 flex-1">
        <ProgressCircle progress={70} size={300} strokeWidth={16} />
        <p className="text-2xl">You're almost done!</p>
      </div>
    </div>
  );
};
