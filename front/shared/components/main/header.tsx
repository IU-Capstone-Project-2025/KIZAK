import React from "react";
import { Bell, Info } from "lucide-react";
import { MainButton } from "./button";

interface Props {
  className?: string;
  user_name: string;
}

export const MainTop: React.FC<Props> = ({ className = "", user_name }) => {
  return (
    <header className={`flex-between h-[50px] ${className}`}>
      <h1 className="text-ui-muted px-2 py-1 bg-ui-dark/90 rounded-lg text-3xl cursor-default">
        {user_name}/<span className="text-brand-primary">Main page</span>
      </h1>
      <div className="flex-between gap-x-2"></div>
    </header>
  );
};
