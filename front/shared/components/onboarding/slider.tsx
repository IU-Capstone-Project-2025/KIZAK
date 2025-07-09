"use client";
import React, { useMemo } from "react";
import { ArrowLeft } from "lucide-react";
import { OnboardingData, SkillLevels } from "@/shared/types/types";

interface SliderLevelProps {
  tag: string;
  skillLevel?: SkillLevels;
  onNext: () => void;
  setData: (data: React.SetStateAction<OnboardingData>) => void;
  onBack: () => void;
}

const levels: SkillLevels[] = ["Beginner", "Intermediate", "Advanced"];

export const SliderLevel: React.FC<SliderLevelProps> = ({
  tag,
  skillLevel = "Intermediate",
  onNext,
  setData,
  onBack,
}) => {
  const [levelIndex, setLevelIndex] = React.useState(() =>
    levels.indexOf(skillLevel)
  );

  const leftPercent = useMemo(
    () => (levelIndex / (levels.length - 1)) * 100,
    [levelIndex]
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    setData((prev) => {
      const filteredSkills = prev.skills.filter((s) => s.skill !== tag);
      return {
        ...prev,
        skills: [
          ...filteredSkills,
          { skill: tag, skill_level: levels[levelIndex], is_goal: false },
        ],
      };
    });
    onNext();
  };

  return (
    <article className="w-100 max-w-md mx-auto space-y-6 bg-white rounded p-6">
      <h2 className="text-center text-lg font-medium text-ui-dark">
        What is your{" "}
        <span className="inline-flex items-center border border-ui-border rounded px-3 py-1 shadow-sm text-sm font-mono">
          {tag}
        </span>{" "}
        level?
      </h2>
      <div className="relative w-full mt-8">
        <div className="h-[10px] bg-gray-200 rounded-full relative">
          <div
            className="absolute h-full bg-brand-primary rounded-full transition-all duration-300"
            style={{ width: `${leftPercent}%` }}
          />
        </div>
        <input
          type="range"
          min={0}
          max={levels.length - 1}
          step={1}
          value={levelIndex}
          onChange={(e) => setLevelIndex(parseInt(e.target.value))}
          className="w-full appearance-none bg-transparent absolute top-0 left-0 h-10 cursor-pointer opacity-0 z-10"
        />
        <div
          className="absolute top-[5px] -translate-y-1/2 h-4 w-4 rounded-full bg-yellow-500 transition-all duration-300 pointer-events-none"
          style={{
            left: `calc(${leftPercent}% - 8px)`,
          }}
        />
        <div className="flex justify-between mt-4 text-sm font-medium text-gray-700">
          {levels.map((level, index) => (
            <span
              key={level}
              className={`${
                index === levelIndex
                  ? "text-yellow-500 font-semibold"
                  : "text-gray-500"
              }`}
            >
              {level}
            </span>
          ))}
        </div>
      </div>
      <div className="flex-between gap-x-1">
        <button
          onClick={onBack}
          className={`h-[50px] flex-center gap-x-2 w-50 py-2 bg-bg-main border border-ui-border shadow-sm hover:bg-bg-subtle text-ui-dark/70 font-semibold rounded-md transition-all duration-300`}
          type="button"
        >
          <ArrowLeft size={18} /> Back
        </button>

        <button
          type="submit"
          onClick={handleSubmit}
          className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 bg-brand-primary hover:bg-brand-primary/90`}
        >
          Continue
        </button>
      </div>
    </article>
  );
};
