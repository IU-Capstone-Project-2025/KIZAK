import React from "react";
import { TaskItem } from "../taskItem";

interface Props {
  className?: string;
}

export const MainTasks: React.FC<Props> = ({ className = "" }) => {
  return (
    <div
      className={`w-full h-1/2 rounded-xl border flex flex-col border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        Last opened
      </h2>
      <div className="flex-1 flex flex-col gap-y-1 py-2">
        <TaskItem done={true} title={"Learn HTML"} />
        <TaskItem done={true} title={"Learn CSS"} />
        <TaskItem done={false} title={"Learn JS"} />
        <TaskItem done={false} title={"Learn TS"} />
      </div>
    </div>
  );
};
