"use client";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import { SignUp } from "@/shared/components/onboarding/signup";
import { Tags } from "@/shared/components/onboarding/tagsQuiz";
import { SliderLevel } from "@/shared/components/onboarding/slider";
import { SingleString } from "@/shared/components/onboarding/singleString";
import { BigString } from "@/shared/components/onboarding/bigString";
import router, { useRouter } from "next/navigation";

const availableSkills = [
  "javascript",
  "typescript",
  "react",
  "vue",
  "angular",
  "nodejs",
  "python",
  "java",
  "php",
  "ruby",
  "go",
  "rust",
];

export type SkillLevels = "Beginner" | "Intermediate" | "Advanced";

export interface ChosenSkill {
  skill: string;
  skillLevel: SkillLevels;
}

export interface OnboardingData {
  login: string;
  password: string;
  background: string;
  education: string;
  skills: string[];
  skills_level: { [skill: string]: SkillLevels };
  goal_skills: string[];
  goals: string[];
  goal_vacancy: string;
}

export default function OnBoarding() {
  const [userData, setUserData] = useState<OnboardingData>({
    login: "",
    password: "",
    background: "",
    education: "",
    skills: [],
    skills_level: {},
    goal_skills: [],
    goals: [],
    goal_vacancy: "",
  });

  const [step, setStep] = useState<number>(0);
  const [displayedStep, setDisplayedStep] = useState<number>(0);
  const [animating, setAnimating] = useState<boolean>(false);
  const router = useRouter();

  const goToNextStep = () => {
    if (step < screens.length - 1) {
      setAnimating(true);
      setTimeout(() => {
        setStep((prev) => prev + 1);
        setDisplayedStep((prev) => prev + 1);
        setAnimating(false);
      }, 300);
    } else {
      router.push("/main/123");
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

  const generateSkillLevelScreens = () => {
    return userData.skills.map((skill) => (
      <SliderLevel
        key={skill}
        tag={skill}
        setData={setUserData}
        onNext={goToNextStep}
        onBack={goToPreviousStep}
      />
    ));
  };

  const screens = [
    <SignUp
      setData={setUserData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
      userData={userData}
    />,
    <SingleString
      title="What is your highest level of education completed?"
      placeholder="Enter your education level..."
      fieldKey="education"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <BigString
      title="Tell us about your background"
      placeholder="Enter your background..."
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <Tags
      tags={availableSkills}
      title="Tell us about your skills"
      placeholder="Enter your skills..."
      singleChoice={false}
      fieldKey="skills"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <SingleString
      title="Which position are you aiming to achieve?"
      placeholder="Enter your vacancy..."
      fieldKey="goal_vacancy"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <Tags
      tags={availableSkills}
      title="Which goal skills are you aiming to achieve?"
      placeholder="Enter your skills..."
      singleChoice={false}
      fieldKey="goal_skills"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <SingleString
      title="Which goals are you aiming to achieve?"
      placeholder="Enter your goals..."
      fieldKey="goals"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    ...generateSkillLevelScreens().map((component) =>
      React.cloneElement(component, { onBack: goToPreviousStep })
    ),
  ];

  const totalSteps = screens.length;

  useEffect(() => {
    console.log(userData);
  }, [step]);

  return (
    <div className="flex items-center justify-center min-h-screen h-full w-142 bg-white">
      <div className="w-full flex-center flex-col space-y-6 bg-white h-200 rounded overflow-hidden">
        <div className="flex justify-center mb-4">
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

        <div
          className={`
            transition-all duration-300 transform
            ${
              animating
                ? "opacity-0 translate-y-4"
                : "opacity-100 translate-y-0"
            }
          `}
        >
          {screens[displayedStep]}
        </div>

        <div className="flex w-100 mx-auto items-center gap-2 justify-between absolute mb-20 bottom-0 left-0 right-0 px-4">
          {Array.from({ length: totalSteps }).map((_, index) => (
            <div
              key={index}
              className={`
                w-3 h-3 rounded-full transition-all duration-300 ${
                  index < step
                    ? "bg-black"
                    : index === step
                    ? "bg-yellow-500"
                    : "bg-gray-300"
                }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
