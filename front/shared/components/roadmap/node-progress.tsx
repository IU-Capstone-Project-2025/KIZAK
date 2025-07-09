import React from "react";
import { Progress } from "./node";

interface Props {
  progress: Progress;
}

const progressColors: Record<Progress, string> = {
  Done: "text-[#3F9965]",
  "In progress": "text-[#D0B16C]",
  "Not started": "text-[#636363]",
};

export const NodeProgress: React.FC<Props> = ({ progress }) => {
  return (
    <p
      className={`text-xs px-3 py-1 border border-ui-border rounded-lg transition-all duration-300 cursor-default hover:bg-bg-subtle ${progressColors[progress]}`}
    >
      {progress}
    </p>
  );
};
