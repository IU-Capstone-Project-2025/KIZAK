import React from "react";

interface Props {
  className?: string;
}

export const MainRoadmap: React.FC<Props> = ({ className = "" }) => {
  return (
    <section
      className={`w-full min-h-100 rounded-xl border border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-lg w-full pl-3 py-1 border-b border-ui-border">
        Roadmap
      </h2>
    </section>
  );
};
