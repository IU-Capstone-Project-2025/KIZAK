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
      <h2 className="text-ui-dark text-sm w-full pl-2 py-0.5 border-b border-ui-border">
        User profile
      </h2>
      <div className="flex flex-col m-1 flex-1 overflow-auto">
        <div className="w-full flex flex-col items-center gap-y-2 mt-4 mb-2">
          {userImage ? (
            <Image
              src={userImage}
              alt={userName}
              width={240}
              height={240}
              className="rounded-2xl w-24 h-24 object-cover border border-ui-border shadow-md"
            />
          ) : (
            <div className="rounded-2xl bg-brand-primary w-24 h-24 border border-ui-border shadow-md" />
          )}
          <div className="flex flex-col items-center mt-2">
            <p className="font-semibold text-sm mb-1">User name</p>
            <p className="bg-bg-subtle w-fit text-sm px-2 py-1 rounded-md border border-ui-border text-center">
              {userName}
            </p>
            <p className="font-semibold text-sm mb-1 mt-3">User goal</p>
            <p className="bg-bg-subtle text-sm px-2 py-1 rounded-md text-center border border-ui-border">
              {userGoal}
            </p>
          </div>
        </div>
        <div className="flex w-full h-fit mt-2 flex-col">
          <div className="text-center w-full text-sm font-semibold">Skill tags</div>
          <div className="h-full w-full flex flex-wrap justify-center gap-1 mt-1">
            {tags.map((tag) => (
              <div
                key={tag}
                className="flex items-center w-fit h-fit border border-ui-border rounded px-2 py-1 shadow-sm transition-all duration-200 hover:bg-bg-subtle text-xs"
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
