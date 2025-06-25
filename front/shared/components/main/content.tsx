import React from "react";
import { MainTop } from "./header";
import { MainRoadmap } from "./roadmap-main";
import { MainProgress } from "./progress";
import { MainChat } from "./chat";
import { MainTasks } from "./tasks";
import { MainCat } from "./cat";
import { TransitionLink } from "../transition/transition-link";

interface Props {
  className?: string;
  userId: string;
}

export const MainContent: React.FC<Props> = ({ className = "", userId }) => {
  return (
    <div className={`h-full flex flex-col gap-y-4 ${className}`}>
      <MainTop />
      <TransitionLink href={`/roadmap/${userId}`}>
        <MainRoadmap />
      </TransitionLink>
      <div className="h-full flex gap-x-4" hidden>
        <MainProgress />
        <MainChat />
        <div className="w-1/3 h-full flex flex-col gap-y-3">
          <MainTasks />
          <MainCat />
        </div>
      </div>
    </div>
  );
};
