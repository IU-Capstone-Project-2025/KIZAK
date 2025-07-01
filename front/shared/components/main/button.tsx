import React, { PropsWithChildren } from "react";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
}

const baseClasses =
  "h-[50px] w-[50px] rounded-xl shadow-sm flex-center transition-all duration-100 cursor-pointer";
export const MainButton: React.FC<PropsWithChildren<Props>> = ({
  className = "",
  children,
  ...rest
}) => {
  return (
    <button
      {...rest}
      className={`${baseClasses} text-ui-dark border border-ui-border hover:bg-bg-subtle ${className}`}
    >
      {children}
    </button>
  );
};
