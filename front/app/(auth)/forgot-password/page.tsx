
"use client";

import React, { useState } from "react";
import { API_BASE_URL } from "@/shared/types/types";

export default function ForgotPassword() {
  const [login, setLogin] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSendResetLink = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/password-reset-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mail: login }),
      });
      if (!res.ok) {
        let errorText = "Failed to send reset link";
        try {
          const errorData = await res.clone().json();
          errorText = errorData.detail
            ? errorData.detail
            : JSON.stringify(errorData);
        } catch {
          try {
            errorText = await res.text();
          } catch {}
        }
        throw new Error(errorText);
      }
      setMessage("Check your email for a password reset link.");
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
        <form className="space-y-4 flex-center flex-col" onSubmit={handleSendResetLink}>
          <input
            type="text"
            placeholder="Enter your email ..."
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            required
          />
          <button
            type="submit"
            disabled={loading || !login}
            className={`h-[50px] w-100 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              login && !loading
                ? "bg-brand-primary hover:bg-brand-primary/90"
                : "bg-brand-primary/80 cursor-not-allowed"
            }`}
          >
            {loading ? "Sending..." : "Send reset link"}
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
