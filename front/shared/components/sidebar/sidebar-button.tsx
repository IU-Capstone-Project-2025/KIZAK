import React, { PropsWithChildren, useState } from "react";
import { TransitionLink } from "../transition/transition-link";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  isActive?: boolean;
  isUser?: boolean;
  href?: string;
  delay?: number;
  tooltip?: string;
}

const baseClasses =
  "h-[55px] w-[55px] rounded-xl flex-center transition-all duration-200 cursor-pointer relative";
const activeClasses =
  "bg-white shadow-[0px_0px_6px_2px_rgba(255,_255,_255,_0.25)] shadow-white text-ui-dark";
const inactiveClasses = "text-white hover:shadow-white hover:text-ui-dark";
const userIcon = "hover:shadow-[0px_0px_4px_1px_rgba(255,_255,_255,_0.1)]";
const notUserIcon =
  "hover:bg-white/90 hover:shadow-[0px_0px_4px_1px_rgba(255,_255,_255,_0.25)]";

export const SidebarButton: React.FC<PropsWithChildren<Props>> = ({
  className = "",
  isActive = false,
  isUser = false,
  children,
  href,
  delay = 0,
  tooltip,
  ...rest
}) => {
  const [hovered, setHovered] = useState(false);

  const content = (
    <>
      {children}
      {tooltip && hovered && (
        <div
          className="absolute left-full top-1/2 -translate-y-1/2 ml-2 whitespace-nowrap rounded bg-black text-white text-xs px-2 py-1 shadow-lg select-none pointer-events-none"
          style={{ zIndex: 1000 }}
        >
          {tooltip}
        </div>
      )}
    </>
  );

  if (href) {
    return (
      <TransitionLink
        delay={delay}
        {...rest}
        href={href}
        className={`${baseClasses} ${
          isActive ? activeClasses : inactiveClasses
        } ${isUser ? userIcon : notUserIcon} ${className}`}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {content}
      </TransitionLink>
    );
  } else {
    return (
      <button
        {...rest}
        className={`${baseClasses} ${
          isActive ? activeClasses : inactiveClasses
        } ${isUser ? userIcon : notUserIcon} ${className}`}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {content}
      </button>
    );
  }
};
