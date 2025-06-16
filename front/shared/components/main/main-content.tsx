import React from "react";
import { MainTop } from "./main-top";
import { MainRoadmap } from "./main-roadmap";
import { MainProgress } from "./main-progress";
import { MainChat } from "./main-chat";
import { MainTasks } from "./main-tasks";
import { MainCat } from "./main-cat";

interface Props {
  className?: string;
}

export const MainContent: React.FC<Props> = ({ className = "" }) => {
  return (
    <div className={`h-full flex flex-col gap-y-4 ${className}`}>
      <MainTop />
      <MainRoadmap />
      <div className="h-full flex gap-x-4">
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
