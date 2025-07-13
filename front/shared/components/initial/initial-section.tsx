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
    <div className="w-full py-16 px-4 bg-ui-dark/95 text-white flex flex-col items-center gap-y-12">
      <h2 className="font-bold text-4xl text-center">{title}</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl w-full">
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
