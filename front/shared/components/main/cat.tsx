import React from "react";
import Image from "next/image";
import catImage from "../../../public/cat.jpg";

interface Props {
  className?: string;
}

export const MainCat: React.FC<Props> = ({ className = "" }) => {
  return (
    <div
      className={`relative bg-[url(/cat.jpg)] bg-cover bg-center shadow-sm rounded-xl overflow-hidden ${className}`}
    ></div>
  );
};
