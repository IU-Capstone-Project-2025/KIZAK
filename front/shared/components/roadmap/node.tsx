import { forwardRef } from "react";
import { NodeProgress } from "./node-progress";

export type Progress = "Done" | "In progress" | "Not started";

interface Props {
  className?: string;
  title: string;
  description: string;
  progress: Progress;
}

export const RoadmapNode = forwardRef<HTMLDivElement, Props>(
  ({ className = "", title, description, progress }, ref) => {
    return (
      <article
        ref={ref}
        className={`w-fit min-w-90 max-w-130 min-h-18 max-h-24 p-4 rounded-lg bg-white border border-ui-border flex flex-col gap-y-1 ${className}`}
      >
        <div className="flex-between">
          <h3 className="font-medium text-[15px] text-ui-dark">{title}</h3>
          <NodeProgress progress={progress} />
        </div>
        <p className="text-ui-dark/80 text-sm font-light">{description}</p>
      </article>
    );
  }
);
RoadmapNode.displayName = "RoadmapNode";
