"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import { ProgressDots } from "@/shared/components/onboarding";
import { getScreens } from "@/shared/utils/getScreens";
import { usePageTransition } from "@/shared/components/transition/transition-provider";
import { API_BASE_URL, OnboardingData } from "@/shared/types/types";

interface OnBoardingProps {
  isEditing?: boolean;
  userId?: string;
}

export function OnBoardingEdit({ isEditing = false, userId }: OnBoardingProps) {
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

  const [userData, setUserData] = useState<OnboardingData>(defaultUserData);
  const [skillOrder, setSkillOrder] = useState<string[] | null>(null);
  const [loading, setLoading] = useState<boolean>(isEditing);
  const [step, setStep] = useState<number>(0);
  const [displayedStep, setDisplayedStep] = useState<number>(0);
  const [animating, setAnimating] = useState<boolean>(false);
  const { handleClick } = usePageTransition();

  useEffect(() => {
    if (isEditing && userId) {
      fetch(`${API_BASE_URL}/users/${userId}/`)
        .then((res) => res.json())
        .then((data) => {
          const loadedData: OnboardingData = {
            login: data.login,
            password: "",
            mail: data.mail || "",
            background: data.background || "",
            education: data.education || "",
            skills: data.skills || [],
            goals: data.goals || "",
            goal_vacancy: data.goal_vacancy || "",
          };
          setUserData(loadedData);
          setLoading(false);
        })
        .catch((err) => {
          console.error("Failed to load user profile", err);
          setLoading(false);
        });
    }
  }, [isEditing, userId]);

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
    if (!isEditing && typeof window !== "undefined") {
      const savedUserData = localStorage.getItem("onboardingUserData");
      const savedStep = localStorage.getItem("onboardingStep");

      if (savedUserData) {
        const parsed = JSON.parse(savedUserData);
        setUserData(parsed);

        const order = parsed.skills
          .filter((s: any) => !s.is_goal)
          .map((s: any) => s.skill);
        setSkillOrder(order);
      }

      if (savedStep) {
        setStep(Number(savedStep));
        setDisplayedStep(Number(savedStep));
      }
    }
  }, [isEditing]);

  useEffect(() => {
    if (!isEditing && typeof window !== "undefined") {
      localStorage.setItem("onboardingUserData", JSON.stringify(userData));
    }
  }, [userData, isEditing]);

  useEffect(() => {
    if (!isEditing && typeof window !== "undefined") {
      localStorage.setItem("onboardingStep", String(step));
    }
  }, [step, isEditing]);

  async function hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }

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
        if (isEditing && userId) {
          const updatedUserData = {
            background: userData.background,
            education: userData.education,
            skills: userData.skills,
            goals: userData.goals,
            goal_vacancy: userData.goal_vacancy,
            user_id: userId,
          };

          const response = await fetch(`${API_BASE_URL}/users/`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updatedUserData),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to update profile");
          }

          handleClick(`/main/${userId}`, 0);
          return;
        }

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
            errorText = errorData.detail
              ? JSON.stringify(errorData.detail)
              : JSON.stringify(errorData);
          } catch {
            errorText = await response.text();
          }
          throw new Error(errorText);
        }

        const data = await response.json();

        if (typeof window !== "undefined") {
          localStorage.removeItem("onboardingUserData");
          localStorage.removeItem("onboardingStep");
        }

        handleClick(`/main/${data.user_id}`, 0);
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

  if (loading || !skillOrder) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Загрузка данных...</p>
      </div>
    );
  }

  const screens = getScreens(
    userData,
    setUserData,
    goToNextStep,
    goToPreviousStep,
    isEditing,
    userId!,
    skillOrder
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
