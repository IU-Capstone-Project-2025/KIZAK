"use client";
import React from "react";
import Image from "next/image";
import { SidebarButton } from "./sidebar-button";
import { Bolt, House, LogOut, Map } from "lucide-react";
const userProfile = "/userProfile.jpg";
import { TransitionLink } from "../transition/transition-link";
import { useParams } from "next/navigation";
import { useRouter } from "next/navigation";

interface Props {
  className?: string;
}

export const Sidebar: React.FC<Props> = ({ className = "" }) => {
  const { user_id } = useParams() as { user_id?: string };
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/log-in");
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
          <SidebarButton href={`/main/${user_id}`}>
            <House width={32} height={33} strokeWidth={1.8} />
          </SidebarButton>
          {/* <SidebarButton href={`/main/${user_id}`}>
            <MessageCircle width={32} height={32} strokeWidth={1.8} />
          </SidebarButton> */}
          <SidebarButton href={`/roadmap/${user_id}`} delay={2000}>
            <Map width={32} height={30} strokeWidth={1.8} />
          </SidebarButton>
        </div>
        <div className="flex flex-col justify-between gap-y-1 items-center">
          <SidebarButton isUser={true}>
            <Image
              width={55}
              height={55}
              src={userProfile}
              alt={"userProfile"}
              className="rounded-xl"
            />
          </SidebarButton>
          <SidebarButton>
            <Bolt width={30} height={32} strokeWidth={1.8} />
          </SidebarButton>
          {/* Кнопка выхода */}
          <SidebarButton onClick={handleLogout}>
            <LogOut width={30} height={30} strokeWidth={1.8} />
          </SidebarButton>
        </div>
      </div>
    </aside>
  );
};
