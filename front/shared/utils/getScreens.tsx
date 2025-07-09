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
  goToPreviousStep: () => void
) => {
  const generateSkillLevelScreens = () => {
    return userData.skills
      .filter((s) => s.is_goal === false)
      .map((skill) => (
        <SliderLevel
          key={`skill_level_${skill.skill}`}
          tag={skill.skill}
          setData={setUserData}
          onNext={goToNextStep}
          onBack={goToPreviousStep}
        />
      ));
  };
  return [
    <SignUp
      key="signup"
      setData={setUserData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
      userData={userData}
    />,
    <SingleString
      key="education"
      title="What is your highest level of education completed?"
      placeholder="Enter your education level..."
      fieldKey="education"
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
    />,
    <BigString
      key="background"
      title="Tell us about your background"
      placeholder="Enter your background..."
      setData={setUserData}
      userData={userData}
      onNext={goToNextStep}
      onBack={goToPreviousStep}
      fieldKey={"background"}
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
    />,
    ...generateSkillLevelScreens().map((screen, index, arr) =>
      React.cloneElement(screen, {
        isLastStep: index === arr.length - 1,
      })
    ),
  ];
};
