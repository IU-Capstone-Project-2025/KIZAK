"use client";
import {
  API_BASE_URL,
  OnboardingData,
  SkillLevels,
  UserSkill,
} from "@/shared/types/types";
import { ArrowLeft } from "lucide-react";
import React, { useEffect, useState } from "react";

interface TagsProps {
  title: string;
  placeholder: string;
  singleChoice: boolean;
  isGoal: boolean;
  setData: (value: React.SetStateAction<OnboardingData>) => void;
  userData: OnboardingData;
  onNext: () => void;
  onBack: () => void;
}

export const Tags: React.FC<TagsProps> = ({
  title,
  placeholder,
  singleChoice,
  setData,
  userData,
  isGoal,
  onNext,
  onBack,
}) => {
  const [allTags, setAllTags] = useState<string[]>([]);
  const [skills, setSkills] = useState<UserSkill[]>([]);
  const [text, setText] = useState<string>("");
  const [filteredSkills, setFilteredSkills] = useState<string[]>([]);
  const [showDropdown, setShowDropdown] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const isValid = skills.length > 0 && !error;

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/skills_list/`);
        const data: string[] = await response.json();
        setAllTags(data);
      } catch (err) {
        console.error("Failed to load skills:", err);
      }
    };
    fetchSkills();
  }, []);

  useEffect(() => {
    setSkills(userData.skills.filter((s) => s.is_goal === isGoal));
  }, [userData, isGoal]);

  useEffect(() => {
    const oppositeSkills = userData.skills
      .filter((s) => s.is_goal !== isGoal)
      .map((s) => s.skill);
    const hasConflict = skills.some((s) => oppositeSkills.includes(s.skill));
    setError(hasConflict ? "Skill tags and Goal tags must not overlap" : "");
  }, [skills, userData.skills, isGoal]);

  function handleAcceptData() {
    if (!isValid) return;
    setData((prev) => {
      const filtered = prev.skills.filter((s) => s.is_goal !== isGoal);
      return {
        ...prev,
        skills: [...filtered, ...skills],
      };
    });
    onNext();
  }

  const handleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setText(value);

    if (value.trim()) {
      const filt = allTags.filter((skill) =>
        skill.toLowerCase().includes(value.toLowerCase().trim())
      );
      setFilteredSkills(filt);
      setShowDropdown(filt.length > 0);
    } else {
      setFilteredSkills([]);
      setShowDropdown(false);
    }
  };

  const handleChooseTag = (tag: string) => {
    const conflictingTags = userData.skills
      .filter((s) => s.is_goal !== isGoal)
      .map((s) => s.skill);

    if (skills.some((s) => s.skill === tag) || conflictingTags.includes(tag)) {
      return;
    }

    setSkills((prev) => {
      const newSkill: UserSkill = {
        skill: tag,
        is_goal: isGoal,
        skill_level: "Beginner" as SkillLevels,
      };

      return singleChoice ? [newSkill] : [...prev, newSkill];
    });

    setText("");
    setShowDropdown(false);
  };

  const handleRemoveSkill = (tag: string) => {
    setSkills((prev) => prev.filter((s) => s.skill !== tag));
  };

  return (
    <article className="w-100 space-y-6 bg-white rounded p-4">
      <h2 className="text-center text-lg font-medium text-ui-dark">{title}</h2>

      <div className="space-y-4 w-full flex flex-col items-center">
        <div className="relative w-full">
          <input
            type="text"
            value={text}
            placeholder={placeholder}
            className="h-[50px] w-full px-4 py-2 border rounded-sm focus:outline-none focus:ring border-ui-border placeholder:text-ui-muted"
            onChange={handleChangeInput}
          />

          <ul
            className={`absolute z-10 w-full py-1 bg-white border border-ui-border rounded-lg mt-2 transition-all duration-200 overflow-y-auto max-h-100 ${
              showDropdown
                ? "opacity-100 scale-100 visible"
                : "opacity-0 scale-95 invisible"
            } origin-top`}
          >
            {filteredSkills.map((skill) => {
              const isAlreadyChosen =
                skills.some((s) => s.skill === skill) ||
                userData.skills.some(
                  (s) => s.skill === skill && s.is_goal !== isGoal
                );

              return (
                <li key={skill} className="w-full">
                  <button
                    type="button"
                    onClick={() => handleChooseTag(skill)}
                    disabled={isAlreadyChosen}
                    className={`w-full text-left px-4 py-2 transition ${
                      isAlreadyChosen
                        ? "text-ui-muted cursor-not-allowed"
                        : "hover:bg-bg-subtle text-ui-dark"
                    }`}
                  >
                    {skill}
                    {isAlreadyChosen && " (already selected)"}
                  </button>
                </li>
              );
            })}
          </ul>
        </div>

        <div className="min-h-8 max-w-full flex flex-wrap justify-center gap-2">
          {skills.map((skill) => (
            <button
              key={skill.skill}
              type="button"
              onClick={() => handleRemoveSkill(skill.skill)}
              className="flex items-center border border-ui-border rounded px-3 py-1 shadow-sm transition-all duration-200 hover:bg-bg-subtle text-sm"
            >
              {skill.skill}
            </button>
          ))}
        </div>

        <div className="flex-between gap-x-1">
          <button
            onClick={onBack}
            className="h-[50px] flex-center gap-x-2 w-50 py-2 bg-bg-main border border-ui-border shadow-sm hover:bg-bg-subtle text-ui-dark/70 font-semibold rounded-md transition-all duration-300"
            type="submit"
          >
            <ArrowLeft size={18} /> Back
          </button>

          <button
            type="submit"
            disabled={!isValid}
            onClick={handleAcceptData}
            className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              isValid ? "bg-brand-primary" : "bg-ui-muted/90 cursor-not-allowed"
            }`}
          >
            Continue
          </button>
        </div>

        {error && <div className="text-red-500 text-xs mt-2">{error}</div>}
      </div>
    </article>
  );
};
