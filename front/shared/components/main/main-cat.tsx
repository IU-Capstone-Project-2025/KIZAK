import React from "react";
import Image from "next/image";
import catImage from "../../../public/cat.jpg";

interface Props {
  className?: string;
}

export const MainCat: React.FC<Props> = ({ className = "" }) => {
  return (
    <div className={`w-full h-1/2 rounded-xl ${className}`}>
      <Image
        className="object-cover w-full h-full rounded-xl"
        src={catImage}
        alt={"catImage"}
      ></Image>
    </div>
  );
};
