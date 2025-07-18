"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import { ProgressDots } from "@/shared/components/onboarding";
import { getScreens } from "@/shared/utils/getScreens";
import { usePageTransition } from "@/shared/components/transition/transition-provider";
import { API_BASE_URL, OnboardingData } from "@/shared/types/types";

export default function OnBoarding() {
  const defaultUserData: OnboardingData = {
    login: "",
    password: "",
    mail: "",
    background: "",
    education: "",
    skills: [],
    goals: "",
    goal_vacancy: "",
  };

  async function hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
    return hashHex;
  }

  const [userData, setUserData] = useState<OnboardingData>(defaultUserData);
  const [step, setStep] = useState<number>(0);
  const [displayedStep, setDisplayedStep] = useState<number>(0);
  const [animating, setAnimating] = useState<boolean>(false);
  const { handleClick } = usePageTransition();
  const [skillOrder, setSkillOrder] = useState<string[] | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const currentSkills = userData.skills
      .filter((s) => !s.is_goal)
      .map((s) => s.skill);

    if (!skillOrder) {
      setSkillOrder(currentSkills);
      return;
    }

    const newSkills = currentSkills.filter((s) => !skillOrder.includes(s));
    if (newSkills.length > 0) {
      setSkillOrder((prev) => [...(prev || []), ...newSkills]);
    }

    const removedSkills = skillOrder.filter((s) => !currentSkills.includes(s));
    if (removedSkills.length > 0) {
      setSkillOrder((prev) =>
        (prev || []).filter((s) => currentSkills.includes(s))
      );
    }
  }, [userData.skills]);

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
        setErrorMessage(null);
        const hashedPassword = await hashPassword(userData.password);
        const payload = { ...userData, password: hashedPassword };

        const response = await fetch(`${API_BASE_URL}/users/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          let errorText = "Ошибка при создании пользователя";
          try {
            const errorData = await response.json();
            if (
              errorData.detail &&
              typeof errorData.detail === "string" &&
              errorData.detail.includes("Email already registered")
            ) {
              errorText = "Email already registered";
            } else {
              errorText = errorData.detail
                ? JSON.stringify(errorData.detail)
                : JSON.stringify(errorData);
            }
          } catch {
            errorText = await response.text();
          }
          setErrorMessage(errorText);
          return;
        }

        const data = await response.json();
        const userId = data.user_id;
        if (typeof window !== "undefined") {
          localStorage.removeItem("onboardingUserData");
          localStorage.removeItem("onboardingStep");
        }
        handleClick(`/main/${userId}?tutorial=1`, 300);
      } catch (error) {
        setErrorMessage("Registration failed. Please try again.");
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
    goToPreviousStep,
    false,
    "",
    skillOrder || []
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
        {errorMessage && (
          <div className="text-red-600 text-center text-sm mb-2">
            {errorMessage}
          </div>
        )}
        <section className={animating ? "fade-slide-out" : "fade-slide-in"}>
          {screens[displayedStep]}
        </section>

        <ProgressDots totalSteps={screens.length} currentStep={step} />
      </div>
    </div>
  );
}
