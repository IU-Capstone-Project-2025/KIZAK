import React, { PropsWithChildren } from "react";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  isActive?: boolean;
  isUser?: boolean;
}

const baseClasses =
  "h-[55px] w-[55px] rounded-xl flex-center transition-all duration-100 cursor-pointer";
const activeClasses =
  "bg-white shadow-[0px_0px_6px_2px_rgba(255,_255,_255,_0.25)] shadow-white text-ui-dark";
const inactiveClasses = "text-white hover:shadow-white hover:text-ui-dark";
const userIcon =
  "hover:bg-white hover:shadow-[0px_0px_4px_1px_rgba(255,_255,_255,_0.1)]";
const notUserIcon =
  "hover:bg-white hover:shadow-[0px_0px_6px_2px_rgba(255,_255,_255,_0.25)]";
export const SidebarButton: React.FC<PropsWithChildren<Props>> = ({
  className = "",
  isActive = false,
  isUser = false,
  children,
  ...rest
}) => {
  return (
    <button
      {...rest}
      disabled={isActive}
      className={`${baseClasses} ${
        isActive ? activeClasses : inactiveClasses
      } ${isUser ? userIcon : notUserIcon} ${className}`}
    >
      {children}
    </button>
  );
};
