"use client";
import React, { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { API_BASE_URL } from "@/shared/types/types";

export default function PasswordResetConfirmPage() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const router = useRouter();
  const params = useParams();
  const token = params.token as string;

  async function hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    setError(null);
    setPasswordError(null);
    if (newPassword.length < 6) {
      setPasswordError("Password must be at least 6 characters long");
      setLoading(false);
      return;
    }
    try {
      const hashedNewPassword = await hashPassword(newPassword);
      const hashedConfirmNewPassword = await hashPassword(confirmNewPassword);
      const res = await fetch(
        `${API_BASE_URL}/password-reset-confirm/${token}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            new_password: hashedNewPassword,
            confirm_new_password: hashedConfirmNewPassword,
          }),
        }
      );
      if (!res.ok) {
        let data;
        try {
          data = await res.json();
        } catch {
          data = {};
        }
        throw new Error(data.detail || "Failed to reset password");
      }
      setMessage("Password reset successfully! You can now log in.");
      setTimeout(() => router.push("/log-in"), 2000);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || "Unknown error");
      } else {
        setError("Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  const isValid = newPassword.length >= 6 && confirmNewPassword.length >= 6;

  useEffect(() => {
    if (newPassword.length > 0 && newPassword.length < 6) {
      setPasswordError("Password must be at least 6 characters long");
    } else {
      setPasswordError(null);
    }
  }, [newPassword]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <div className="w-full max-w-sm space-y-6 bg-white rounded">
        <h2 className="text-center text-lg font-medium text-ui-dark mb-4">
          Set a new password
        </h2>
        <form
          className="space-y-4 flex-center flex-col"
          onSubmit={handleSubmit}
        >
          <input
            type="password"
            placeholder="New password"
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          {passwordError && (
            <div className="text-red-600 text-center text-sm mb-2">
              {passwordError}
            </div>
          )}
          <input
            type="password"
            placeholder="Confirm new password"
            className="h-[50px] placeholder:text-ui-muted w-100 px-4 py-2 border rounded-sm focus:outline-none border-ui-border"
            value={confirmNewPassword}
            onChange={(e) => setConfirmNewPassword(e.target.value)}
            required
          />
          <button
            type="submit"
            disabled={loading || !isValid || !!passwordError}
            className={`h-[50px] w-100 py-2 text-white font-semibold rounded-md transition-all duration-300 ${
              isValid && !loading && !passwordError
                ? "bg-brand-primary hover:bg-brand-primary/90"
                : "bg-brand-primary/80 cursor-not-allowed"
            }`}
          >
            {loading ? "Resetting..." : "Reset Password"}
          </button>
        </form>
        {message && <div className="text-green-600 text-center">{message}</div>}
        {error && <div className="text-red-600 text-center">{error}</div>}
      </div>
    </div>
  );
}
