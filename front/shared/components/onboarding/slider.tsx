"use client";
import React, { useMemo, useState } from "react";
import { ArrowLeft } from "lucide-react";
import { OnboardingData, SkillLevels } from "@/shared/types/types";

interface SliderLevelProps {
  tag: string;
  skillLevel?: SkillLevels;
  onNext: () => void;
  setData: (data: React.SetStateAction<OnboardingData>) => void;
  onBack: () => void;
  isLastStep?: boolean;
}

const levels: SkillLevels[] = ["Beginner", "Intermediate", "Advanced"];

export const SliderLevel: React.FC<SliderLevelProps> = ({
  tag,
  skillLevel = "Intermediate",
  onNext,
  setData,
  onBack,
  isLastStep = false,
}) => {
  const [levelIndex, setLevelIndex] = useState(() =>
    levels.indexOf(skillLevel)
  );
  const [isSubmitting, setIsSubmitting] = useState(false);

  const leftPercent = useMemo(
    () => (levelIndex / (levels.length - 1)) * 100,
    [levelIndex]
  );

  const handleSubmit = async (e: React.FormEvent) => {
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

    if (isLastStep) {
      setIsSubmitting(true);
    }

    await new Promise((res) => setTimeout(res, 50));
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
          style={{ left: `calc(${leftPercent}% - 8px)` }}
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
          className="h-[50px] flex-center gap-x-2 w-50 py-2 bg-bg-main border border-ui-border shadow-sm hover:bg-bg-subtle text-ui-dark/70 font-semibold rounded-md transition-all duration-300"
          type="button"
        >
          <ArrowLeft size={18} /> Back
        </button>

        <button
          type="submit"
          onClick={handleSubmit}
          disabled={isSubmitting}
          className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 flex items-center justify-center ${
            isSubmitting
              ? "bg-brand-primary/70 cursor-not-allowed"
              : "bg-brand-primary hover:bg-brand-primary/90"
          }`}
        >
          {isSubmitting ? (
            <svg
              className="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-20"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-80"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
              />
            </svg>
          ) : (
            "Continue"
          )}
        </button>
      </div>
    </article>
  );
};
