import React from "react";
import { ReactElement } from "react";
interface Props {
  title: string;
  description: string;
  icon: ReactElement;
}

export const InitialCard: React.FC<Props> = ({ title, description, icon }) => {
  return (
    <div
      className={`h-65 w-55 px-4 rounded-sm bg-white text-ui-dark flex-center flex-col text-center`}
    >
      <div className="w-full h-[30%] flex-center">{icon}</div>
      <h3 className="font-medium text-lg mb-4">{title}</h3>
      <p className="font-light text-sm">{description}</p>
    </div>
  );
};
