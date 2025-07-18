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
    let trimmedText =
      description.length > 100
        ? description.slice(0, 100).trim() + "..."
        : description;

    const wrapTextByWords = (text: string, maxLength: number): string => {
      const words = text.split(" ");
      let lines: string[] = [];
      let currentLine = "";

      for (const word of words) {
        if ((currentLine + " " + word).trim().length <= maxLength) {
          currentLine += (currentLine ? " " : "") + word;
        } else {
          lines.push(currentLine);
          currentLine = word;
        }
      }
      if (currentLine) lines.push(currentLine);

      return lines.join("\n");
    };

    const formattedDescription = wrapTextByWords(trimmedText, 50);

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
            whiteSpace: "pre-line"
          }}
        >
          {formattedDescription}
        </p>
      </article>
    );
  }
);
RoadmapNode.displayName = "RoadmapNode";