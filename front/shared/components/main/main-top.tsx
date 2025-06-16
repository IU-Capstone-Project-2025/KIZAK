import React from "react";
import { Bell, Info, MessageCircle } from "lucide-react";
import { MainButton } from "./main-button";

interface Props {
  className?: string;
}

export const MainTop: React.FC<Props> = ({ className = "" }) => {
  return (
    <header className={`flex-between h-[50px] ${className}`}>
      <h1 className="text-ui-muted px-2 py-1 bg-ui-dark/90 rounded-lg text-3xl cursor-default">
        project-name/<span className="text-brand-primary">Main page</span>
      </h1>
      <div className="flex-between gap-x-2">
        <MainButton>
          <Bell width={26} height={27} strokeWidth={1.8} />
        </MainButton>
        <MainButton>
          <Info width={26} height={26} strokeWidth={1.8} />
        </MainButton>
      </div>
    </header>
  );
};
