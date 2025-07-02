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
