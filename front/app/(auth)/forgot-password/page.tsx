
"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/shared/types/types";

export default function ForgotPassword() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  async function hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    setError(null);
    try {
      const hashedPassword = await hashPassword(password);
      const res = await fetch(`${API_BASE_URL}/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login, password: hashedPassword }),
      });
      if (!res.ok) {
        let errorText = "Failed to reset password";
        try {
          // Try to parse as JSON first
          const errorData = await res.clone().json();
          errorText = errorData.detail
            ? errorData.detail
            : JSON.stringify(errorData);
        } catch {
          try {
            errorText = await res.text();
          } catch {
            // fallback
          }
        }
        throw new Error(errorText);
      }
      setMessage("Password reset successful! You can now log in.");
      setTimeout(() => router.push("/log-in"), 2000);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <div className="w-full max-w-sm space-y-6 bg-white rounded">
        <h2 className="text-center text-lg font-medium text-ui-dark mb-4">
          Reset your password
        </h2>
        <form className="space-y-4 flex-center flex-col" onSubmit={handleReset}>
          <input
            type="text"
            placeholder="Enter your login..."
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Enter your new password..."
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="submit"
            disabled={loading || !login || !password}
            className={`h-[50px] w-100 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              login && password && !loading
                ? "bg-brand-primary hover:bg-brand-primary/90"
                : "bg-brand-primary/80 cursor-not-allowed"
            }`}
          >
            {loading ? "Resetting..." : "Reset Password"}
          </button>
        </form>
        {message && <div className="text-green-600 text-center">{message}</div>}
        {error && <div className="text-red-600 text-center">{error}</div>}
        <div className="flex justify-center mt-4">
          <a
            href="/log-in"
            className="text-xs text-ui-muted hover:underline"
          >
            Back to login
          </a>
        </div>
      </div>
    </div>
  );
} 
