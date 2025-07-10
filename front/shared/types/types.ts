export const API_URL = `https://${process.env.API_HOST}:${process.env.API_PORT}`;

export type SkillLevels = "Beginner" | "Intermediate" | "Advanced";

export interface ChosenSkill {
  skill: string;
  skillLevel: SkillLevels;
}

export interface UserSkill {
  skill: string;
  skill_level: SkillLevels;
  is_goal: boolean;
}

export interface OnboardingData {
  login: string;
  password: string;
  background: string;
  education: string;
  goals: string;
  goal_vacancy: string;
  skills: UserSkill[];
}
export type Progress = "Done" | "In progress" | "Not started";

export interface RawNode {
  node_id: string;
  title: string;
  summary: string;
}

export interface RawLink {
  from_node: string;
  to_node: string;
}
