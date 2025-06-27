import React from "react";
import { RoadmapMini } from "../roadmap/roadmap-mini";

interface Props {
  className?: string;
}

export const MainRoadmap: React.FC<Props> = ({ className = "" }) => {
  return (
    <section
      className={`flex flex-col w-full min-h-100 h-100 rounded-xl group border shadow-sm border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-start text-lg w-full pl-3 py-1 border-b border-ui-border">
        Roadmap
      </h2>
      <div className="flex-1 w-full dots relative">
        <div className="rounded-b-xl absolute z-10 inset-0 transition-all duration-300 group-hover:bg-black/3" />
        <RoadmapMini />
      </div>
    </section>
  );
};
