import React from "react";

interface Props {
  className?: string;
}

export const MainTasks: React.FC<Props> = ({ className = "" }) => {
  return (
    <div
      className={`w-full h-1/2 rounded-xl border border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        Last opened
      </h2>
    </div>
  );
};
