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
  onNext: (updatedData: OnboardingData) => void;
  onBack: () => void;
  isLastStep?: boolean;
}

export const BigString: React.FC<Props> = ({
  title,
  placeholder,
  setData,
  userData,
  onNext,
  onBack,
  fieldKey,
  isLastStep = false,
}) => {
  const [text, setText] = useState<string>(
    typeof userData[fieldKey] === "string" ? (userData[fieldKey] as string) : ""
  );
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isValid = text.trim() !== "";

  async function handleAcceptData() {
    if (!isValid) return;

    const updatedData = { ...userData, [fieldKey]: text };
    setData(updatedData);

    if (isLastStep) {
      setIsSubmitting(true);
      await new Promise((res) => setTimeout(res, 50));
    }

    onNext(updatedData);
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
            disabled={isSubmitting}
          >
            <ArrowLeft size={18} /> Back
          </button>

          <button
            type="button"
            disabled={!isValid || isSubmitting}
            onClick={handleAcceptData}
            className={`h-[50px] w-50 py-2 text-white font-semibold rounded-md transition-all duration-300 flex items-center justify-center ${
              isValid && !isSubmitting
                ? "bg-brand-primary"
                : "bg-ui-muted/90 cursor-not-allowed"
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
      </div>
    </article>
  );
};
