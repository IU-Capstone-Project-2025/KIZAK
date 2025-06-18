import { Circle, CircleCheck } from "lucide-react";
import React from "react";

interface Props {
  done: boolean;
  title: string;
}

export const TaskItem: React.FC<Props> = ({ done, title }) => {
  return (
    <button
      className={`w-full px-4 h-10 text-ui-dark flex items-center gap-x-3 text-xl font-light transition-all duration-300 cursor-pointer hover:bg-bg-subtle`}
    >
      {done ? (
        <CircleCheck size={32} color="#3F9965" />
      ) : (
        <Circle size={32} color="#DDDDDD" />
      )}
      <p>{title}</p>
    </button>
  );
};
