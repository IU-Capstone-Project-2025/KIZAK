import React from "react";
import { useInView } from "@/shared/hooks/useInView";

interface Props {
  title: string;
  description: string;
  icon: React.ReactElement;
}

export const InitialCard: React.FC<Props> = ({ title, description, icon }) => {
  const { ref, isVisible } = useInView();

  return (
    <div
      ref={ref}
      className={`bg-[#1a1a1a] rounded-2xl p-6 flex flex-col items-center text-center gap-4 shadow-md transition-all duration-500 ease-out transform
        ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}
        hover:shadow-xl hover:-translate-y-1 hover:bg-[#232323] group`}
    >
      <div className="text-primary transition-transform duration-300 group-hover:scale-110">
        {icon}
      </div>
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-sm text-gray-300">{description}</p>
    </div>
  );
};
