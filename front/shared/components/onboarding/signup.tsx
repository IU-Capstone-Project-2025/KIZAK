"use client";
import { API_BASE_URL, OnboardingData } from "@/shared/types/types";
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
  const [mail, setMail] = useState(userData.mail || "");
  const [loginError, setLoginError] = useState<string>("");
  const [passwordError, setPasswordError] = useState<string>("");
  const [mailError, setMailError] = useState<string>("");
  const [checkingLogin, setCheckingLogin] = useState(false);
  const [mailChecking, setMailChecking] = useState(false);
  const debounceTimeout = useRef<NodeJS.Timeout | null>(null);

  async function checkLoginExists(login: string) {
    setCheckingLogin(true);
    try {
      const res = await fetch(`${API_BASE_URL}/check_login/${login}`);
      const data = await res.json();
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

  async function checkMailExists(mail: string) {
    setMailChecking(true);
    try {
      const res = await fetch(
        `${API_BASE_URL}/check_email/${encodeURIComponent(mail)}`
      );
      const data = await res.json();
      if (data.exists) {
        setMailError("Email already registered");
      } else {
        setMailError("");
      }
    } catch {
      setMailError("Error checking email");
    } finally {
      setMailChecking(false);
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

  useEffect(() => {
    if (mail.trim() === "") {
      setMailError("");
      setMailChecking(false);
      return;
    }
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }
    debounceTimeout.current = setTimeout(() => {
      checkMailExists(mail);
    }, 300);

    return () => {
      if (debounceTimeout.current) {
        clearTimeout(debounceTimeout.current);
      }
    };
  }, [mail]);

  function handleAcceptData() {
    let valid = true;
    setLoginError("");
    setPasswordError("");
    setMailError("");

    if (login.trim() === "") {
      setLoginError("Login is required");
      valid = false;
    }

    if (password.trim().length < 6) {
      setPasswordError("Password must be at least 6 characters");
      valid = false;
    }

    if (mail.trim() === "") {
      setMailError("Email is required");
      valid = false;
    } else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail.trim())) {
      setMailError("Invalid email format");
      valid = false;
    }

    if (valid) {
      setData((prev) => ({
        ...prev,
        login: login,
        password: password,
        mail: mail,
      }));
      onNext();
    }
  }

  const isValid =
    login.trim() !== "" &&
    password.trim().length >= 6 &&
    mail.trim() !== "" &&
    /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail.trim()) &&
    !loginError &&
    !passwordError &&
    !mailError &&
    !checkingLogin &&
    !mailChecking;

  return (
    <article className="w-full max-w-sm space-y-6 bg-white rounded">
      <h2 className="text-center text-lg font-medium text-ui-dark">
        Create your account
      </h2>

      <div className="space-y-4 flex-center flex-col">
        <input
          type="email"
          placeholder="Enter your email..."
          className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring border-ui-border"
          value={mail}
          onChange={(e) => setMail(e.target.value)}
        />
        {mailError && <div className="text-red-500 text-xs">{mailError}</div>}
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
            isValid ? "bg-brand-primary" : "bg-ui-muted/90 cursor-not-allowed"
          }`}
        >
          {checkingLogin || mailChecking ? "Checking..." : "Continue"}
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
