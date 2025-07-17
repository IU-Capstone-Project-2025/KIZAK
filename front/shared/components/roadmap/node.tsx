import { forwardRef } from "react";
import { NodeProgress } from "./node-progress";

export type Progress = "Done" | "In progress" | "Not started";

interface Props {
  className?: string;
  title: string;
  description: string;
  progress: Progress;
  onClick?: () => void;
}

export const RoadmapNode = forwardRef<HTMLDivElement, Props>(
  ({ className = "", title, description, progress, onClick }, ref) => {
    return (
      <article
        onClick={onClick}
        ref={ref}
        className={`w-fit min-w-90 min-h-18 p-4 rounded-lg bg-white border border-[#DDDDDD] flex flex-col gap-y-1 ${className}`}
      >
        <div className="flex items-center justify-between gap-x-4">
          <h3 className="font-medium text-[15px] text-ui-dark">{title}</h3>
          <NodeProgress progress={progress} />
        </div>
        <p
          className="text-ui-dark/80 text-sm font-light roadmap-preview-description"
          style={{
            whiteSpace: 'pre-line',
            overflow: 'visible',
          }}
        >
          {description}
        </p>
      </article>
    );
  }
);
RoadmapNode.displayName = "RoadmapNode";
