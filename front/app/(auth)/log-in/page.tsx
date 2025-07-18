"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
import { TransitionLink } from "@/shared/components/transition/transition-link";
import { usePageTransition } from "@/shared/components/transition/transition-provider";
import { API_BASE_URL } from "@/shared/types/types";

export default function Login() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [isValid, setValid] = useState<boolean>(false);
  const { handleClick } = usePageTransition();

  useEffect(() => {
    setValid(login.trim() !== "" && password.trim() !== "");
  }, [login, password]);

  async function hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const hashedPassword = await hashPassword(password);

      const formData = new URLSearchParams();
      formData.append("grant_type", "password");
      formData.append("username", login);
      formData.append("password", hashedPassword);

      const res = await fetch(`${API_BASE_URL}/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!res.ok) {
        let errorText = "Ошибка при входе";
        try {
          const errorData = await res.json();
          errorText = errorData.detail
            ? JSON.stringify(errorData.detail)
            : JSON.stringify(errorData);
        } catch {
          errorText = await res.text();
        }
        throw new Error(errorText);
      }

      const data = await res.json();
      const userId = data.user_id;
      handleClick(`/main/${userId}`, 0);
    } catch (error) {
      console.error("Ошибка при входе:", error);
      alert("Неверный логин или пароль");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <div className="w-full max-w-sm space-y-6 bg-white rounded">
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

        <h2 className="text-center text-lg font-medium text-ui-dark">
          Log in to your account
        </h2>

        <form className="space-y-4 flex-center flex-col" onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Enter your login..."
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
          />
          <input
            type="password"
            placeholder="Enter your password..."
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="submit"
            disabled={!isValid}
            className={`h-[50px] w-100 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              isValid
                ? "bg-brand-primary hover:bg-brand-primary/90"
                : "bg-brand-primary/80 cursor-not-allowed"
            }`}
          >
            Log in
          </button>
        </form>

        <div className="flex justify-between text-xs text-ui-muted w-full mt-4">
          <TransitionLink
            delay={100}
            href="/onboarding"
            className="hover:underline"
          >
            or Sign up
          </TransitionLink>
          <TransitionLink
            delay={100}
            href="/forgot-password"
            className="hover:underline"
          >
            Forgot your password?
          </TransitionLink>
        </div>
      </div>
    </div>
  );
}
