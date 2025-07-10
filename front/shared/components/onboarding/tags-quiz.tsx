"use client";
import { OnboardingData, UserSkill } from "@/shared/types/types";
import { ArrowLeft } from "lucide-react";
import React, { useEffect, useState } from "react";
import { Portal } from "../Portal";

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
  const inputRef = React.useRef<HTMLInputElement>(null);
  const [dropdownStyle, setDropdownStyle] = useState<React.CSSProperties>({});

  const isValid = skills.length > 0;

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await fetch("http://localhost:8000/skills_list/");
        const data: string[] = await response.json();
        setAllTags(data);
      } catch (err) {
        console.error("Failed to load skills:", err);
      }
    };

    fetchSkills();
  }, []);

  useEffect(() => {
    const uniqueSkills = userData.skills.filter((s, idx, arr) =>
      arr.findIndex(u => u.skill === s.skill && u.is_goal === s.is_goal) === idx && s.is_goal === isGoal
    );
    setSkills(uniqueSkills);
  }, [userData, isGoal]);

  useEffect(() => {
    const allSkills = isGoal
      ? userData.skills.filter((s) => !s.is_goal).map((s) => s.skill)
      : userData.skills.filter((s) => s.is_goal).map((s) => s.skill);
    const overlap = skills.some((s) => allSkills.includes(s.skill));
    if (overlap) {
      setError("Skill tags and Goal tags must not overlap");
    } else {
      setError("");
    }
  }, [skills, userData.skills, isGoal]);

  function handleAcceptData() {
    if (error) return;
    if (isValid) {
      setData({ ...userData, skills: [...userData.skills, ...skills] });
      onNext();
    }
  }

  const handleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setText(value);

    if (value.trim().length > 0) {
      const filt = allTags.filter((skill) =>
        skill.toLowerCase().includes(value.toLowerCase().trim())
      );
      setFilteredSkills(filt);
      setShowDropdown(true);
      // Calculate dropdown position
      setTimeout(() => {
        if (inputRef.current) {
          const rect = inputRef.current.getBoundingClientRect();
          setDropdownStyle({
            position: "absolute",
            top: rect.bottom + window.scrollY,
            left: rect.left + window.scrollX,
            width: rect.width,
            zIndex: 9999,
          });
        }
      }, 0);
    } else {
      setFilteredSkills([]);
      setShowDropdown(false);
    }
  };

  const handleChooseTag = (tag: string) => {
    if (singleChoice) {
      setSkills([{ skill: tag, is_goal: isGoal, skill_level: "Beginner" }]);
    } else {
      if (!skills.some((s) => s.skill === tag)) {
        setSkills((prev) => [
          ...prev,
          { skill: tag, is_goal: isGoal, skill_level: "Beginner" },
        ]);
      }
    }

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
        <div className="relative w-full z-50">
          <input
            ref={inputRef}
            type="text"
            value={text}
            placeholder={placeholder}
            className="h-[50px] w-full px-4 py-2 border rounded-sm focus:outline-none focus:ring border-ui-border placeholder:text-ui-muted"
            onChange={handleChangeInput}
          />

          {showDropdown && filteredSkills.length > 0 && (
            <Portal>
              <ul
                style={dropdownStyle}
                className={`py-1 bg-white border border-ui-border rounded-lg mt-2 transition-all duration-200 overflow-y-auto max-h-100 ${
                  showDropdown && filteredSkills.length > 0
                    ? "opacity-100 scale-100 visible"
                    : "opacity-0 scale-95 invisible"
                } origin-top`}
              >
                {filteredSkills.map((skill) => (
                  <li key={skill} className="w-full">
                    <button
                      type="button"
                      onClick={() => handleChooseTag(skill)}
                      className="w-full text-left px-4 py-2 hover:bg-bg-subtle text-ui-dark transition"
                    >
                      {skill}
                    </button>
                  </li>
                ))}
              </ul>
            </Portal>
          )}
        </div>

        <div className="min-h-8 max-w-full flex flex-wrap justify-center gap-2">
          {[...new Map(skills.map(s => [s.skill + s.is_goal, s])).values()].map((skill) => (
            <button
              key={skill.skill + String(skill.is_goal)}
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
            className={`h-[50px] flex-center gap-x-2 w-50 py-2 bg-bg-main border border-ui-border shadow-sm hover:bg-bg-subtle text-ui-dark/70 font-semibold rounded-md transition-all duration-300`}
            type="submit"
          >
            <ArrowLeft size={18} /> Back
          </button>

          <button
            type="submit"
            disabled={!isValid || !!error}
            onClick={handleAcceptData}
            className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              isValid && !error
                ? "bg-brand-primary"
                : "bg-brand-primary/50 cursor-not-allowed"
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
