export type SkillLevels = "Beginner" | "Intermediate" | "Advanced";

export interface ChosenSkill {
  skill: string;
  skillLevel: SkillLevels;
}

export interface UserSkill {
  skill: string;
  level: SkillLevels;
}

export interface OnboardingData {
  login: string;
  password: string;
  background: string;
  education: string;
  skills: string[];
  skills_level: UserSkill[];
  goal_skills: string[];
  goals: string[];
  goal_vacancy: string;
}
