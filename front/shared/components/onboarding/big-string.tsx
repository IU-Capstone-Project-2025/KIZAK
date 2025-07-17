"use client";
import { OnboardingData } from "@/shared/types/types";
import { ArrowLeft } from "lucide-react";
import React, { useState } from "react";

interface Props {
  title: string;
  placeholder: string;
  setData: (value: React.SetStateAction<OnboardingData>) => void;
  fieldKey: keyof Pick<OnboardingData, "goals" | "background">;
  userData: OnboardingData;
  onNext: () => void;
  onBack: () => void;
}

export const BigString: React.FC<Props> = ({
  title,
  placeholder,
  setData,
  userData,
  onNext,
  onBack,
  fieldKey,
}) => {
  const [text, setText] = useState<string>(
    typeof userData[fieldKey] === "string" ? (userData[fieldKey] as string) : ""
  );

  const isValid = text.trim() !== "";

  function handleAcceptData() {
    if (isValid) {
      setData({ ...userData, [fieldKey]: text });
      onNext();
    }
  }

  return (
    <article className="w-100 max-w-sm space-y-6 bg-white rounded">
      <h2 className="text-center text-lg font-medium text-ui-dark">{title}</h2>

      <div className="space-y-4 flex-center flex-col">
        <textarea
          placeholder={placeholder}
          className="h-60 w-140 resize-none placeholder:text-ui-muted px-4 py-3 border rounded-sm focus:outline-none focus:ring outline-none border-ui-border"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="flex-between gap-x-1">
          <button
            onClick={onBack}
            className="h-[50px] flex-center gap-x-2 w-50 py-2 bg-bg-main border border-ui-border shadow-sm hover:bg-bg-subtle text-ui-dark/70 font-semibold rounded-md transition-all duration-300"
            type="button"
          >
            <ArrowLeft size={18} /> Back
          </button>

          <button
            type="button"
            disabled={!isValid}
            onClick={handleAcceptData}
            className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              isValid ? "bg-brand-primary" : "bg-ui-muted/90 cursor-not-allowed"
            }`}
          >
            Continue
          </button>
        </div>
      </div>
    </article>
  );
};
