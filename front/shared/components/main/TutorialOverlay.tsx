"use client";
import React, { useEffect, useState } from "react";

interface Step {
  selector: string;
  title: string;
  description: string;
}

const steps: Step[] = [
  {
    selector: "#main-roadmap",
    title: "Roadmap",
    description: "Здесь вы увидите свой персональный план развития.",
  },
  {
    selector: "#main-progress",
    title: "Прогресс",
    description: "Следите за выполненными шагами и прогрессом обучения.",
  },
  {
    selector: "#user-profile",
    title: "Профиль",
    description: "Здесь ваш профиль и цели, которые вы указали в онбординге.",
  },
  {
    selector: "#main-tasks",
    title: "Last opened",
    description: "В этом блоке вы найдете последние открытые курсы в родмапе.",
  },
];

export const TutorialOverlay: React.FC<{ onFinish: () => void }> = ({
  onFinish,
}) => {
  const [stepIndex, setStepIndex] = useState(0);
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);
  const [positionAbove, setPositionAbove] = useState(false);

  useEffect(() => {
    const el = document.querySelector(steps[stepIndex].selector);
    if (el) {
      const rect = el.getBoundingClientRect();
      setTargetRect(rect);

      const spaceBelow = window.innerHeight - rect.bottom;
      const tooltipHeight = 130;

      setPositionAbove(spaceBelow < tooltipHeight + 20);
    }
  }, [stepIndex]);

  if (!targetRect) return null;

  const step = steps[stepIndex];

  const nextStep = () => {
    if (stepIndex < steps.length - 1) {
      setStepIndex(stepIndex + 1);
    } else {
      onFinish();
    }
  };

  const tooltipStyle: React.CSSProperties = {
    left: targetRect.left,
    width: 288,
  };

  if (positionAbove) {
    tooltipStyle.top = targetRect.top - 130 - 12;
  } else {
    tooltipStyle.top = targetRect.bottom + 12;
  }

  const left = typeof tooltipStyle.left === "number" ? tooltipStyle.left : 0;

  if (left + 288 > window.innerWidth) {
    tooltipStyle.left = window.innerWidth - 288 - 12;
  }
  if (left < 12) {
    tooltipStyle.left = 12;
  }

  return (
    <>
      <div
        className="fixed inset-0 bg-transparent z-40"
        style={{ pointerEvents: "auto" }}
      />

      <div
        className="fixed z-50 rounded-xl transition-all duration-200"
        style={{
          top: targetRect.top - 8,
          left: targetRect.left - 8,
          width: targetRect.width + 16,
          height: targetRect.height + 16,
          boxShadow: "0 0 0 9999px rgba(0,0,0,0.6)",
          borderRadius: "12px",
          pointerEvents: "none",
        }}
      />

      <div
        className="fixed z-60 transition-all duration-200 bg-white shadow-xl rounded-xl p-4 w-72"
        style={tooltipStyle}
      >
        <h2 className="text-lg font-bold mb-2">{step.title}</h2>
        <p className="text-sm text-gray-600 mb-4">{step.description}</p>
        <div className="flex justify-end gap-2">
          <button
            onClick={onFinish}
            className="px-3 py-1 text-sm rounded bg-gray-200"
          >
            Пропустить
          </button>
          <button
            onClick={nextStep}
            className="px-3 py-1 text-sm rounded bg-yellow-400"
          >
            {stepIndex === steps.length - 1 ? "Готово" : "Дальше"}
          </button>
        </div>
      </div>
    </>
  );
};
