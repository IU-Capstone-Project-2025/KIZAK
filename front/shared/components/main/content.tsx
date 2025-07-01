import React from "react";
import { MainTop } from "./header";
import { MainRoadmap } from "./roadmap-main";
import { MainProgress } from "./progress";
import { MainTasks } from "./tasks";
import { MainCat } from "./cat";
import { TransitionLink } from "../transition/transition-link";
import { UserProfileMain } from "./user-profile-main";

interface Props {
  className?: string;
  userId: string;
}

export const MainContent: React.FC<Props> = ({ className = "", userId }) => {
  return (
    <div className={`h-full flex flex-col gap-y-4 ${className}`}>
      <MainTop />
      <TransitionLink delay={2000} href={`/roadmap/${userId}`}>
        <MainRoadmap />
      </TransitionLink>
      <div className="flex-1 flex flex-wrap gap-4">
        <MainProgress className="flex-1 min-w-[300px]" userId={userId} />
        <UserProfileMain
          userName="netimaaa"
          userImage="/userProfile.jpg"
          className="flex-1 min-w-[300px]"
          userGoal={"Frontend developer"}
          tags={[
            "javascript",
            "typescript1",
            "typescript2",
            "typescript3",
            "typescript4",
          ]}
        />
        <div className="flex-1 flex flex-col gap-y-3 min-w-[300px]">
          <MainTasks className="flex-1" />
          <MainCat className="flex-1" />
        </div>
      </div>
    </div>
  );
};
