"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import Image from "next/image";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isValid, setValid] = useState<boolean>(false);

  useEffect(() => {
    if (email.trim() !== "" && password.trim() !== "") setValid(true);
    else setValid(false);
  }, [email, password]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <div className="w-full max-w-sm space-y-6 bg-white rounded ">
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

        <form className="space-y-4 flex-center flex-col">
          <input
            type="login"
            placeholder="Enter your login..."
            className="h-[50px] placeholder: text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none focus:ring  outline:none border-ui-border"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
            className={`h-[50px] w-100 py-2  hover:bg-brand-primary text-white font-semibold rounded-md transition-all duration-300 ${
              isValid
                ? "bg-brand-primary hover:bg-brand-primary/90"
                : "bg-brand-primary/80 cursor-not-allowed"
            }`}
          >
            Log in
          </button>
        </form>

        <div className="flex justify-between text-xs text-ui-muted w-full mt-4">
          <Link href="/sign-up" className="hover:underline">
            or Sign up
          </Link>
          <a href="#" className="hover:underline">
            Forgot your password?
          </a>
        </div>
      </div>
    </div>
  );
}
