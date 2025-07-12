"use client";

import React, { useEffect, useState } from "react";
import { MainTop } from "./header";
import { MainRoadmap } from "./roadmap-main";
import { MainProgress } from "./progress";
import { MainTasks } from "./tasks";
import { MainCat } from "./cat";
import { TransitionLink } from "../transition/transition-link";
import { UserProfileMain } from "./user-profile-main";
import { API_BASE_URL, Progress } from "@/shared/types/types";

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

  useEffect(() => {
    async function fetchProfile() {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE_URL}/users/profile/${userId}/`);
        if (!res.ok)
          throw new Error(`Failed to fetch profile: ${res.statusText}`);
        const data: ProfileResponse = await res.json();
        setProfile(data);
      } catch (err: any) {
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    }
    fetchProfile();
  }, [userId]);

  if (loading) return <div>Loading user profile...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>No profile data</div>;

  return (
    <div className={`h-full flex flex-col gap-y-4 ${className}`}>
      <MainTop />
      <TransitionLink delay={2000} href={`/roadmap/${userId}`}>
        <MainRoadmap />
      </TransitionLink>
      <div className="flex-1 flex flex-wrap gap-4 h-[45%]">
        <MainProgress
          progress={profile.progress}
          className="flex-1 min-w-[300px]"
          userId={userId}
        />
        <UserProfileMain
          userName={profile.user.login}
          userImage="/userProfile.jpg"
          className="flex-1 min-w-[300px]"
          userGoal={profile.user.goals}
          tags={profile.user.skills.map((s) => s.skill)}
        />
        <div className="flex-1 flex flex-col gap-y-3 min-w-[300px]">
          <MainTasks
            histotyItems={profile.history}
            className="flex-1"
            userId={userId}
          />
          
        </div>
      </div>
    </div>
  );
};
