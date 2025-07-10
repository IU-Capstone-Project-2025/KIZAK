"use client";
import { API_URL, OnboardingData } from "@/shared/types/types";
import React, { useState, useEffect, useRef } from "react";
import { TransitionLink } from "../transition/transition-link";

interface Props {
  setData: (value: React.SetStateAction<OnboardingData>) => void;
  userData: OnboardingData;
  onNext: () => void;
  onBack: () => void;
}

export const SignUp: React.FC<Props> = ({ setData, userData, onNext }) => {
  const [login, setLogin] = useState(userData.login);
  const [password, setPassword] = useState(userData.password);
  const [loginError, setLoginError] = useState<string>("");
  const [passwordError, setPasswordError] = useState<string>("");
  const [checkingLogin, setCheckingLogin] = useState(false);
  const debounceTimeout = useRef<NodeJS.Timeout | null>(null);

  async function checkLoginExists(login: string) {
    setCheckingLogin(true);
    try {
      const res = await fetch(`${API_URL}/check_login/${login}`);
      const data = await res.json();
      console.log(data);
      if (data.exists) {
        setLoginError("Login already exists");
      } else {
        setLoginError("");
      }
    } catch {
      setLoginError("Error checking login");
    } finally {
      setCheckingLogin(false);
    }
  }

  useEffect(() => {
    if (login.trim() === "") {
      setLoginError("");
      setCheckingLogin(false);
      return;
    }
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }
    debounceTimeout.current = setTimeout(() => {
      checkLoginExists(login);
    }, 300);

    return () => {
      if (debounceTimeout.current) {
        clearTimeout(debounceTimeout.current);
      }
    };
  }, [login]);

  function handleAcceptData() {
    let valid = true;
    setLoginError("");
    setPasswordError("");

    if (login.trim() === "") {
      setLoginError("Login is required");
      valid = false;
    }

    if (password.trim().length < 6) {
      setPasswordError("Password must be at least 6 characters");
      valid = false;
    }

    if (valid) {
      setData((prev) => ({
        ...prev,
        login: login,
        password: password,
      }));
      onNext();
    }
  }

  const isValid =
    login.trim() !== "" &&
    password.trim().length >= 6 &&
    !loginError &&
    !checkingLogin;

  return (
    <article className="w-full max-w-sm space-y-6 bg-white rounded">
      <h2 className="text-center text-lg font-medium text-ui-dark">
        Create your account
      </h2>

      <div className="space-y-4 flex-center flex-col">
        <input
          type="text"
          placeholder="Enter your login..."
          value={login}
          className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring border-ui-border"
          onChange={(e) => setLogin(e.target.value)}
        />
        {loginError && <div className="text-red-500 text-xs">{loginError}</div>}

        <input
          type="password"
          placeholder="Enter your password..."
          className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring border-ui-border"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            if (e.target.value.length < 6) {
              setPasswordError("Password must be at least 6 characters");
            } else {
              setPasswordError("");
            }
          }}
        />
        {passwordError && (
          <div className="text-red-500 text-xs">{passwordError}</div>
        )}

        <button
          type="submit"
          disabled={!isValid}
          onClick={handleAcceptData}
          className={`h-[50px] w-100 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
            isValid
              ? "bg-brand-primary"
              : "bg-brand-primary/50 cursor-not-allowed"
          }`}
        >
          {checkingLogin ? "Checking..." : "Continue"}
        </button>
      </div>

      <div className="flex justify-center text-xs text-ui-muted w-full mt-4">
        <TransitionLink delay={300} href="/log-in" className="hover:underline">
          or Log in
        </TransitionLink>
      </div>
    </article>
  );
};
