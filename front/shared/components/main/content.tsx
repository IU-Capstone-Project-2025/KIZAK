"use client";

import React, { useEffect, useState } from "react";
import { MainTop } from "./header";
import { MainRoadmap } from "./roadmap-main";
import { MainProgress } from "./progress";
import { MainTasks } from "./tasks";
import { TransitionLink } from "../transition/transition-link";
import { UserProfileMain } from "./user-profile-main";

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
  history: string[];
}

interface Props {
  className?: string;
  userId: string;
}

export const MainContent: React.FC<Props> = ({ className = "", userId }) => {
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isTallScreen, setIsTallScreen] = useState(false);

  useEffect(() => {
    function handleResize() {
      setIsTallScreen(window.innerHeight > 1100); 
    }
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    async function fetchProfile() {
      try {
        setLoading(true);
        const res = await fetch(
          `http://localhost:8000/users/profile/${userId}/`
        );
        if (!res.ok)
          throw new Error(`Failed to fetch profile: ${res.statusText}`);
        const data: ProfileResponse = await res.json();
        setProfile(data);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Unknown error");
        }
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
    <div className={`h-screen flex flex-col gap-y-2 md:gap-y-4 overflow-hidden ${className}`}>
      <MainTop />
      <TransitionLink delay={2000} href={`/roadmap/${userId}`}>
        <MainRoadmap className={isTallScreen ? "h-[400px]" : "h-[250px]"} />
      </TransitionLink>
      <div className="flex flex-col md:flex-row flex-1 flex-wrap gap-2 md:gap-4 min-h-0">
        <MainProgress
          progress={profile.progress}
          className="w-full md:flex-1 min-w-0 max-h-[220px] md:min-w-[240px] md:max-h-[390px]"
          userId={userId}
        />
        <UserProfileMain
          userName={profile.user.login}
          userImage="/userProfile.jpg"
          className="w-full md:flex-1 min-w-0 max-h-[220px] md:min-w-[240px] md:max-h-[390px]"
          userGoal={profile.user.goals}
          tags={profile.user.skills.map((s) => s.skill)}
        />
        <div className="w-full md:flex-1 flex flex-col gap-y-2 md:gap-y-3 min-w-0 max-h-[220px] md:min-w-[240px] md:max-h-[390px]">
          <MainTasks className="flex-1 min-h-0 max-h-[220px] md:max-h-[390px]" />
        </div>
      </div>
    </div>
  );
};
