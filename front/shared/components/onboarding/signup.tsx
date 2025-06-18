"use client";
import { OnboardingData } from "@/app/(auth)/onboarding/page";
import Link from "next/link";
import React, { useEffect, useState } from "react";

interface Props {
  setData: (value: React.SetStateAction<OnboardingData>) => void;
  userData: OnboardingData;
  onNext: () => void;
  onBack: () => void;
}

export const SignUp: React.FC<Props> = ({
  setData,
  userData,
  onNext,
  onBack,
}) => {
  const [login, setLogin] = useState(userData.login);
  const [password, setPassword] = useState(userData.password);

  const [isValid, setValid] = useState<boolean>(false);

  useEffect(() => {
    setLogin(userData.login);
    setPassword(userData.password);
  }, [userData]);

  function handleAcceptData() {
    if (isValid) {
      setData((prev) => ({
        ...prev,
        login: login,
        password: password,
      }));
      onNext();
    }
  }

  useEffect(() => {
    if (login.trim() !== "" && password.trim() !== "") setValid(true);
    else setValid(false);
  }, [login, password]);

  return (
    <div className="w-full max-w-sm space-y-6 bg-white rounded ">
      <h2 className="text-center text-lg font-medium text-ui-dark">
        Create your account
      </h2>

      <div className="space-y-4 flex-center flex-col">
        <input
          type="login"
          placeholder="Enter your login..."
          value={login}
          className="h-[50px] placeholder: text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring  outline:none border-ui-border"
          onChange={(e) => setLogin(e.target.value)}
        />
        <input
          type="password"
          placeholder="Enter your password..."
          className="h-[50px] placeholder: text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring  outline:none border-ui-border"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          disabled={!isValid}
          onClick={handleAcceptData}
          className={`h-[50px] w-100 py-2 hover:bg-brand-primary text-white font-semibold rounded-md transition-all duration-300 ${
            isValid
              ? "bg-brand-primary hover:bg-brand-primary/90"
              : "bg-brand-primary/80 cursor-not-allowed"
          }`}
        >
          Continue
        </button>
      </div>

      <div className="flex justify-center text-xs text-ui-muted w-full mt-4">
        <Link href="/log-in" className="hover:underline">
          or Log in
        </Link>
      </div>
    </div>
  );
};
