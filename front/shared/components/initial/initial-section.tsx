import React from "react";
import { InitialCard } from "./initial-card";

interface CardData {
  title: string;
  description: string;
  icon: React.ReactElement;
}

interface Props {
  title: string;
  cards: CardData[];
}

export const InitialSection: React.FC<Props> = ({ title, cards }) => {
  return (
    <div className="w-full h-fit py-10 bg-ui-dark text-white flex-center flex-col gap-y-12">
      <h2 className="font-bold text-3xl">{title}</h2>
      <div className="flex items-center w-[60%] justify-between">
        {cards.map((card, index) => (
          <InitialCard
            key={index}
            title={card.title}
            description={card.description}
            icon={card.icon}
          />
        ))}
      </div>
    </div>
  );
};
