import React from "react";
import Image from "next/image";
import { SidebarButton } from "./sidebar-button";
import { Bolt, Folder, House, LogOut, Map, MessageCircle } from "lucide-react";
import userProfile from "../../../public/userProfile.jpg";
import Link from "next/link";

interface Props {
  className?: string;
}

export const Sidebar: React.FC<Props> = ({ className = "" }) => {
  return (
    <aside className={`h-full w-[90px] ${className}`}>
      <div className="h-full bg-ui-dark rounded-xl flex flex-col justify-between py-7">
        <Link
          href={"/"}
          className="pb-7 border-b border-white mx-4 px-1 flex-center"
        >
          <Image src={"/logo.svg"} alt={"KIZAK"} width={50} height={50} />
        </Link>
        <div className="flex flex-col justify-between gap-y-2 items-center">
          <SidebarButton isActive={true}>
            <House width={32} height={33} strokeWidth={1.8} />
          </SidebarButton>
          <SidebarButton>
            <MessageCircle width={32} height={32} strokeWidth={1.8} />
          </SidebarButton>
          <SidebarButton>
            <Map width={32} height={30} strokeWidth={1.8} />
          </SidebarButton>
          <SidebarButton>
            <Folder width={32} height={29} strokeWidth={1.8} />
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
          <SidebarButton>
            <LogOut width={30} height={30} strokeWidth={1.8} />
          </SidebarButton>
        </div>
      </div>
    </aside>
  );
};
