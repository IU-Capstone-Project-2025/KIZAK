"use client";
import React, { useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { OnboardingData } from "@/shared/types/types";
import { ProgressDots } from "@/shared/components/onboarding";
import { getScreens } from "@/shared/utils/getScreens";
import { usePageTransition } from "@/shared/components/transition/transition-provider";

export default function OnBoarding() {
  const [userData, setUserData] = useState<OnboardingData>({
    login: "",
    password: "",
    background: "",
    education: "",
    skills: [],
    skills_level: [],
    goal_skills: [],
    goals: [],
    goal_vacancy: "",
  });

  const [step, setStep] = useState<number>(0);
  const [displayedStep, setDisplayedStep] = useState<number>(0);
  const [animating, setAnimating] = useState<boolean>(false);
  const { handleClick } = usePageTransition();

  const goToNextStep = () => {
    if (step < screens.length - 1) {
      setAnimating(true);
      setTimeout(() => {
        setStep((prev) => prev + 1);
        setDisplayedStep((prev) => prev + 1);
        setAnimating(false);
      }, 300);
    } else {
      handleClick("/main/123");
    }
  };

  const goToPreviousStep = () => {
    if (step > 0) {
      setAnimating(true);
      setTimeout(() => {
        setStep((prev) => prev - 1);
        setDisplayedStep((prev) => prev - 1);
        setAnimating(false);
      }, 300);
    }
  };

  const screens = getScreens(
    userData,
    setUserData,
    goToNextStep,
    goToPreviousStep
  );

  return (
    <div className="flex items-center justify-center min-h-screen h-full w-142 bg-white">
      <div className="w-full flex-center flex-col space-y-6 bg-white h-200 rounded overflow-hidden">
        <div
          className={`flex justify-center mb-4 transition-all duration-300 transform
            ${
              animating
                ? "opacity-0 translate-y-[10px]"
                : "opacity-100 translate-y-0"
            }`}
        >
          <div className="w-18 h-18 rounded-full flex items-center justify-center">
            <div className="w-18 h-18 rounded-full relative overflow-hidden">
              <Image
                src="/logo.svg"
                alt="KIZAK"
                layout="fill"
                objectFit="contain"
              />
            </div>
          </div>
        </div>

        <section className={animating ? "fade-slide-out" : "fade-slide-in"}>
          {screens[displayedStep]}
        </section>

        <ProgressDots totalSteps={screens.length} currentStep={step} />
      </div>
    </div>
  );
}
