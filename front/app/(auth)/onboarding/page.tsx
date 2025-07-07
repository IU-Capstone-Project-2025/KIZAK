"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import { ProgressDots } from "@/shared/components/onboarding";
import { getScreens } from "@/shared/utils/getScreens";
import { usePageTransition } from "@/shared/components/transition/transition-provider";
import { OnboardingData } from "@/shared/types/types";

export default function OnBoarding() {
  const defaultUserData: OnboardingData = {
    login: "",
    password: "",
    background: "",
    education: "",
    skills: [],
    goals: "",
    goal_vacancy: "",
  };

  const [userData, setUserData] = useState<OnboardingData>(defaultUserData);
  const [step, setStep] = useState<number>(0);
  const [displayedStep, setDisplayedStep] = useState<number>(0);
  const [animating, setAnimating] = useState<boolean>(false);
  const { handleClick } = usePageTransition();

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedUserData = localStorage.getItem("onboardingUserData");
      if (savedUserData) setUserData(JSON.parse(savedUserData));

      const savedStep = localStorage.getItem("onboardingStep");
      if (savedStep) {
        setStep(Number(savedStep));
        setDisplayedStep(Number(savedStep));
      }
    }
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("onboardingUserData", JSON.stringify(userData));
    }
  }, [userData]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("onboardingStep", String(step));
    }
  }, [step]);

  const goToNextStep = async () => {
    if (step < screens.length - 1) {
      setAnimating(true);
      setTimeout(() => {
        setStep((prev) => prev + 1);
        setDisplayedStep((prev) => prev + 1);
        setAnimating(false);
      }, 300);
    } else {
      try {
        const response = await fetch("http://localhost:8000/users/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          let errorText = "Ошибка при создании пользователя";
          try {
            const errorData = await response.json();
            errorText = errorData.detail
              ? JSON.stringify(errorData.detail)
              : JSON.stringify(errorData);
          } catch {
            errorText = await response.text();
          }
          throw new Error(errorText);
        }

        const data = await response.json();
        const userId = data.user_id;
        if (typeof window !== "undefined") {
          localStorage.removeItem("onboardingUserData");
          localStorage.removeItem("onboardingStep");
        }
        handleClick(`/main/${userId}`, 300);
      } catch (error) {
        console.error("Ошибка при завершении онбординга:", error);
      }
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
          className={`flex justify-center mb-4 transition-all duration-300 transform ${
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
