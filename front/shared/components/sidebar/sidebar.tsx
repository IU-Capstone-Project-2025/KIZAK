"use client";
import React from "react";
import Image from "next/image";
import { SidebarButton } from "./sidebar-button";
import { House, LogOut, Map, RefreshCw } from "lucide-react";
const userProfile = "/userProfile.jpg";
import { TransitionLink } from "../transition/transition-link";
import { useParams } from "next/navigation";

interface Props {
  className?: string;
}

export const Sidebar: React.FC<Props> = ({ className = "" }) => {
  const { user_id } = useParams() as { user_id?: string };

  const handleLogout = () => {
    localStorage.removeItem("token");
  };

  return (
    <aside className={`h-full min-w-[90px] w-[90px] ${className}`}>
      <div className="h-full bg-ui-dark rounded-xl flex flex-col justify-between py-7">
        <TransitionLink
          href={"/"}
          className="pb-7 border-b border-white mx-4 px-1 flex-center"
        >
          <Image
            className="transition-all duration-300 hover:scale-105"
            src={"/logo.svg"}
            alt={"KIZAK"}
            width={50}
            height={50}
          />
        </TransitionLink>
        <div className="flex flex-col justify-between gap-y-2 items-center">
          <SidebarButton tooltip="Home" href={`/main/${user_id}`}>
            <House width={32} height={33} strokeWidth={1.8} />
          </SidebarButton>
          {/* <SidebarButton href={`/main/${user_id}`}>
            <MessageCircle width={32} height={32} strokeWidth={1.8} />
          </SidebarButton> */}
          <SidebarButton
            tooltip="Roadmap"
            href={`/roadmap/${user_id}`}
            delay={300}
          >
            <Map width={32} height={30} strokeWidth={1.8} />
          </SidebarButton>
        </div>
        <div className="flex flex-col justify-between gap-y-1 items-center">
          {/* <SidebarButton isUser={true}>
            <Image
              width={55}
              height={55}
              src={userProfile}
              alt={"userProfile"}
              className="rounded-xl"
            />
          </SidebarButton> */}
          <SidebarButton
            tooltip="re-onboarding"
            href={`/onboarding/edit/${user_id}`}
            delay={100}
          >
            <RefreshCw width={30} height={32} strokeWidth={1.8} />
          </SidebarButton>
          <SidebarButton
            tooltip="log-out"
            href={`/log-in`}
            onClick={handleLogout}
            delay={100}
          >
            <LogOut width={30} height={30} strokeWidth={1.8} />
          </SidebarButton>
        </div>
      </div>
    </aside>
  );
};
