import React from "react";

interface Props {
  className?: string;
}

export const MainChat: React.FC<Props> = ({ className = "" }) => {
  return (
    <div
      className={`w-1/3 h-full rounded-xl border border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        Chat with mentor
      </h2>
    </div>
  );
};
