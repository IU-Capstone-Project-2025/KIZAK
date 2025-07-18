import { Circle, CircleCheck, CircleDot } from "lucide-react";
import React from "react";
import { Progress } from "../types/types";
import { TransitionLink } from "./transition/transition-link";

interface Props {
  progress?: Progress;
  title: string;
  userId: string;
  nodeId: string;
}

export const TaskItem: React.FC<Props> = ({
  progress = "Not started",
  title,
  userId,
  nodeId,
}) => {
  return (
    <TransitionLink
      className={`w-full px-4 h-12 py-2 text-ui-dark/80 flex items-center gap-x-3 text-md font-light transition-all duration-300 cursor-pointer hover:bg-bg-subtle hover:text-ui-dark`}
      href={`/roadmap/${userId}/${nodeId}`}
    >
      {progress === "Done" ? (
        <CircleCheck size={26} color="#3F9965" />
      ) : progress === "In progress" ? (
        <CircleDot size={26} color="#ffd883" />
      ) : (
        <Circle size={26} color="#DDDDDD" />
      )}
      <p>{title}</p>
    </TransitionLink>
  );
};
