import React from "react";
import Image from "next/image";
import catImage from "../../../public/cat.jpg";

interface Props {
  className?: string;
}

export const MainCat: React.FC<Props> = ({ className = "" }) => {
  return (
    <div
      className={`relative w-full pt-[56.25%] shadow-sm rounded-xl overflow-hidden ${className}`}
    >
      <Image
        src={catImage}
        alt="Cat"
        fill
        className="object-cover rounded-xl"
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      />
    </div>
  );
};
