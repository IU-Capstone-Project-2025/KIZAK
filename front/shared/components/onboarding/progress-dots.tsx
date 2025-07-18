import React from "react";

interface Props {
  totalSteps: number;
  currentStep: number;
}

export const ProgressDots: React.FC<Props> = ({ totalSteps, currentStep }) => {
  return (
    <div className="flex justify-center items-center gap-6 mt-12 flex-wrap px-4">
      {Array.from({ length: totalSteps }).map((_, index) => (
        <div
          key={index}
          className={`
            w-3 h-3 rounded-full transition-all duration-300
            ${
              index < currentStep
                ? "bg-black"
                : index === currentStep
                ? "bg-yellow-500"
                : "bg-gray-300"
            }
          `}
        />
      ))}
    </div>
  );
};
