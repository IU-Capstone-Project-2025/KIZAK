import React from "react";
import Image from "next/image";

interface Props {
  className?: string;
  userImage?: string;
  userName: string;
  tags: string[];
  userGoal: string;
}

export const UserProfileMain: React.FC<Props> = ({
  className = "",
  userName,
  userImage,
  tags,
  userGoal,
}) => {
  return (
    <div
      className={`rounded-xl flex flex-col shadow-sm border border-ui-border ${className}`}
    >
      <h2 className="text-ui-dark text-md w-full pl-3 py-2 border-b border-ui-border">
        User profile
      </h2>
      <div className="flex flex-col m-10 flex-1">
        <div className="w-full h-1/2 flex gap-x-8 items-start">
          {userImage ? (
            <Image
              src={userImage}
              alt={userName}
              width={240}
              height={240}
              className="rounded-xl"
            />
          ) : (
            <div className="rounded-xl bg-brand-primary w-60 h-60" />
          )}
          <div className="flex flex-col justify-start">
            <p className="font-semibold text-sm mb-2">User name</p>
            <p className="bg-bg-subtle w-fit text-md px-2 py-1 rounded-md border border-ui-border">
              {userName}
            </p>
            <p className="font-semibold text-sm mb-2 mt-4">User goal</p>
            <p className="bg-bg-subtle text-md px-2 py-1 rounded-md text-center border border-ui-border">
              {userGoal}
            </p>
          </div>
        </div>
        <div className="flex w-full h-fit mt-12 flex-col">
          <div className="text-center w-full mt-8 text-xl">Skill tags</div>
          <div className="h-full w-full flex flex-wrap justify-center gap-2 mt-4">
            {tags.map((tag) => (
              <div
                key={tag}
                className="flex items-center w-fit h-fit border border-ui-border rounded px-3 py-1 shadow-sm transition-all duration-200 hover:bg-bg-subtle text-sm"
              >
                {tag}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
