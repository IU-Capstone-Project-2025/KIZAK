import React from "react";
import { OnboardingData } from "../types/types";
import {
  SliderLevel,
  SignUp,
  SingleString,
  BigString,
  Tags,
} from "@/shared/components/onboarding";

export const getScreens = (
  userData: OnboardingData,
  setUserData: React.Dispatch<React.SetStateAction<OnboardingData>>,
  goToNextStep: () => void,
  goToPreviousStep: () => void,
  isEditing: boolean = false,
  userId: string = "",
  skillOrder: string[]
) => {
  const screens = [];

  if (!isEditing) {
    screens.push(
      <SignUp
        key="signup"
        setData={setUserData}
        onNext={goToNextStep}
        onBack={goToPreviousStep}
        userData={userData}
      />
    );
  }

  screens.push(
    <SingleString
      key="education"
      title="What is your highest level of education completed?"
      placeholder="Enter your education level..."
      fieldKey="education"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
      isEditing={isEditing}
      userId={isEditing ? userId : ""}
    />,
    <BigString
      key="background"
      title="Tell us about your background"
      placeholder="Enter your background..."
      fieldKey="background"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <Tags
      key="skills"
      title="Tell us about your skills"
      placeholder="Enter your skills..."
      singleChoice={false}
      isGoal={false}
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <SingleString
      key="goal_vacancy"
      title="Which position are you aiming to achieve?"
      placeholder="Enter your vacancy..."
      fieldKey="goal_vacancy"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <Tags
      key="goal_skills"
      title="Which goal skills are you aiming to achieve?"
      placeholder="Enter your skills..."
      singleChoice={false}
      isGoal={true}
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <BigString
      key="goals"
      title="Which goals are you aiming to achieve?"
      placeholder="Enter your goals..."
      fieldKey="goals"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />
  );

  const generateSkillLevelScreens = () => {
    return skillOrder.map((skillName, index) => {
      const skillData = userData.skills.find(
        (s) => s.skill === skillName && !s.is_goal
      );

      return (
        <SliderLevel
          key={`skill_level_${skillName}`}
          tag={skillName}
          skillLevel={skillData?.skill_level}
          userData={userData}
          setData={setUserData}
          onNext={goToNextStep}
          onBack={goToPreviousStep}
          isLastStep={index === skillOrder.length - 1}
        />
      );
    });
  };

  return [
    ...screens,
    ...generateSkillLevelScreens().map((screen, index, arr) =>
      React.cloneElement(screen, {
        isLastStep: index === arr.length - 1,
      })
    ),
  ];
};
