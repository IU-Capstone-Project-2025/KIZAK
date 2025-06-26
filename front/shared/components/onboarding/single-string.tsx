"use client";
import { OnboardingData } from "@/shared/types/types";
import { ArrowLeft } from "lucide-react";
import React, { useState } from "react";

interface Props {
  title: string;
  placeholder: string;
  setData: (value: React.SetStateAction<OnboardingData>) => void;
  userData: OnboardingData;
  fieldKey: keyof Pick<OnboardingData, "education" | "goal_vacancy" | "goals">;
  onNext: () => void;
  onBack: () => void;
}

export const SingleString: React.FC<Props> = ({
  title,
  placeholder,
  setData,
  userData,
  fieldKey,
  onNext,
  onBack,
}) => {
  const [text, setText] = useState<string>(
    typeof userData[fieldKey] === "string" ? (userData[fieldKey] as string) : ""
  );

  const isValid = typeof text === "string" && text.trim() !== "";

  function handleAcceptData() {
    if (isValid) {
      setData((prev) => ({ ...prev, [fieldKey]: text }));
      onNext();
    }
  }

  return (
    <article className="w-full max-w-sm space-y-6 bg-white rounded ">
      <h2 className="text-center text-lg font-medium text-ui-dark">{title}</h2>

      <div className="space-y-4 flex-center flex-col">
        <input
          type="text"
          placeholder={placeholder}
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring  outline:none border-ui-border"
        />
        <div className="flex-between gap-x-1">
          <button
            onClick={onBack}
            className={`h-[50px] flex-center gap-x-2 w-50 py-2 bg-bg-main border border-ui-border shadow-sm hover:bg-bg-subtle text-ui-dark/70 font-semibold rounded-md transition-all duration-300`}
            type="button"
          >
            <ArrowLeft size={18} /> Back
          </button>

          <button
            type="button"
            disabled={!isValid}
            onClick={handleAcceptData}
            className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              isValid
                ? "bg-brand-primary hover:bg-brand-primary/90"
                : "bg-brand-primary/50 cursor-not-allowed"
            }`}
          >
            Continue
          </button>
        </div>
      </div>
    </article>
  );
};
