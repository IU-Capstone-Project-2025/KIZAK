"use client";

import React, { useEffect, useState } from "react";
import { MainTop } from "./header";
import { MainRoadmap } from "./roadmap-main";
import { MainProgress } from "./progress";
import { MainTasks } from "./tasks";
import { TransitionLink } from "../transition/transition-link";
import { UserProfileMain } from "./user-profile-main";
import { API_BASE_URL, Progress } from "@/shared/types/types";
import { useRouter, useSearchParams } from "next/navigation";
import { TutorialOverlay } from "./TutorialOverlay";

interface UserSkill {
  skill: string;
  skill_level?: string;
  is_goal: boolean;
}

interface UserData {
  login: string;
  background: string;
  education: string;
  goals: string;
  goal_vacancy: string;
  skills: UserSkill[];
  user_id: string;
  creation_date: string;
}

interface ProfileResponse {
  user: UserData;
  roadmap_id: string;
  progress: number;
  history: HistoryItem[];
}

export type HistoryItem = {
  node_id: string;
  title: string;
  progress: Progress;
};

interface Props {
  className?: string;
  userId: string;
}

export const MainContent: React.FC<Props> = ({ className = "", userId }) => {
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTutorial, setShowTutorial] = useState(false);
  const router = useRouter();

  const params = useSearchParams();

  useEffect(() => {
    if (params.get("tutorial") === "1") {
      setShowTutorial(true);
    }
  }, [params]);

  useEffect(() => {
    async function fetchProfile() {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE_URL}/users/profile/${userId}/`);
        if (!res.ok)
          throw new Error(`Failed to fetch profile: ${res.statusText}`);
        const data: ProfileResponse = await res.json();
        setProfile(data);
      } catch (err: unknown) {
        const errorMessage =
          err instanceof Error ? err.message : "Unknown error";
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    }
    fetchProfile();
  }, [userId]);

  const finishTutorial = () => {
    setShowTutorial(false);

    const url = new URL(window.location.href);
    url.searchParams.delete("tutorial");
    router.replace(url.pathname + url.search);
  };

  if (loading) return <div>Loading user profile...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>No profile data</div>;

  return (
    <div className={`h-full flex flex-col gap-y-4 flex-1 ${className}`}>
      <MainTop user_name={profile.user.login} />
      <TransitionLink delay={300} href={`/roadmap/${userId}`}>
        {" "}
        <div id="main-roadmap">
          <MainRoadmap userId={userId} />
        </div>
      </TransitionLink>
      <div className="flex-1 flex flex-wrap gap-4">
        <div className="basis-[300px] grow" id="main-progress">
          <MainProgress
            progress={profile.progress}
            className="h-full flex-1"
            userId={userId}
          />
        </div>
        <div className="basis-[300px] grow" id="user-profile">
          <UserProfileMain
            userName={profile.user.login}
            userImage="/userProfile.jpg"
            className="h-full flex-1"
            userGoal={profile.user.goals}
            tags={profile.user.skills.map((s) => s.skill)}
          />
        </div>
        <div
          id="main-tasks"
          className="flex flex-1 flex-col gap-y-3 basis-[300px] grow"
        >
          <MainTasks
            histotyItems={profile.history}
            className="flex-1"
            userId={userId}
          />
        </div>
      </div>
      {showTutorial && <TutorialOverlay onFinish={finishTutorial} />}
    </div>
  );
};
