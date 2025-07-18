import React from "react";
import { TaskItem } from "../taskItem";
import { HistoryItem } from "./content";

interface Props {
  className?: string;
  histotyItems: HistoryItem[];
  userId: string;
}

export const MainTasks: React.FC<Props> = ({
  className = "",
  histotyItems,
  userId,
}) => {
  return (
    <div
      className={`rounded-xl border flex flex-col shadow-sm border-ui-border overflow-hidden min-h-0 ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        Last opened
      </h2>
      <div className="flex-1 flex flex-col gap-y-2 py-2">
        {histotyItems.map((el) => (
          <TaskItem
            key={el.node_id}
            userId={userId}
            nodeId={el.node_id}
            progress={el.progress || "Not started"}
            title={el.title}
          />
        ))}
      </div>
    </div>
  );
};
