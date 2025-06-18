import React from "react";
import Image from "next/image";
import Link from "next/link";

export const Header = () => {
  return (
    <header className={`flex-between text-ui-dark px-8 py-5`}>
      <div className="w-80">
        <Image width={55} height={55} src={"/logo.svg"} alt={"logo"} />
      </div>
      <p className="uppercase text-3xl font-bold w-80 flex-center">kizak</p>
      <div className="flex items-center justify-end gap-x-5 text-lg w-80">
        <Link className="font-light" href={"/onboarding"}>
          Sign up
        </Link>
        <Link
          className="bg-brand-primary/80 py-2 px-3 rounded-md transition-all duration-300 hover:bg-brand-primary"
          href={"/onboarding"}
        >
          Open app
        </Link>
      </div>
    </header>
  );
};
