import React from "react";

interface Props {
  totalSteps: number;
  currentStep: number;
}

export const ProgressDots: React.FC<Props> = ({ totalSteps, currentStep }) => {
  return (
    <div className="flex w-100 mx-auto items-center gap-2 justify-between absolute mb-20 bottom-0 left-0 right-0 px-4">
      {Array.from({ length: totalSteps }).map((_, index) => (
        <div
          key={index}
          className={`
                w-3 h-3 rounded-full transition-all duration-300 ${
                  index < currentStep
                    ? "bg-black"
                    : index === currentStep
                    ? "bg-yellow-500"
                    : "bg-gray-300"
                }`}
        />
      ))}
    </div>
  );
};
