import React from "react";
import { Roadmap } from "../roadmap/roadmap";

interface Props {
  className?: string;
}

export const MainRoadmap: React.FC<Props> = ({ className = "" }) => {
  return (
    <section
      className={`flex flex-col w-full min-h-100 h-100 rounded-xl border border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-lg w-full pl-3 py-1 border-b border-ui-border">
        Roadmap
      </h2>
      <div className="flex-1 w-full dots">
        <Roadmap />
      </div>
    </section>
  );
};
