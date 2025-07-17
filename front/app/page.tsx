"use client";

import { Header } from "@/shared/components/initial/header";
import { InitialSection } from "@/shared/components/initial/initial-section";
import { useInView } from "@/shared/hooks/useInView";
import Image from "next/image";
import {
  BotMessageSquare,
  BrainCircuit,
  ChartArea,
  FileUser,
  NotebookPen,
  Scroll,
} from "lucide-react";

export default function Page() {
  const cardData1 = [
    {
      title: "Personalized Learning Paths",
      description: "KIZAK doesn’t follow a one-size-fits-all approach",
      icon: <BrainCircuit size={50} strokeWidth={1.8} />,
    },
    {
      title: "Smart Task Recommendations",
      description: "Get the most relevant tasks based on your progress",
      icon: <BotMessageSquare size={50} strokeWidth={1.8} />,
    },
    {
      title: "Continuous AI Support",
      description: "Ask questions and get help anytime with AI mentorship",
      icon: <ChartArea size={50} strokeWidth={1.8} />,
    },
  ];

  const cardData2 = [
    {
      title: "Create Your Profile",
      description: "Tell us your skills, goals, and interests",
      icon: <Scroll width={50} height={52} strokeWidth={1.8} />,
    },
    {
      title: "Get Your Learning Plan",
      description: "Receive a personalized roadmap built by AI",
      icon: <NotebookPen size={50} strokeWidth={1.8} />,
    },
    {
      title: "Build Your AI-Powered Resume",
      description:
        "KIZAK helps you create a job-ready resume based on your real skills and progress",
      icon: <FileUser width={50} height={54} strokeWidth={1.8} />,
    },
  ];

  const { ref: textRef, isVisible: textVisible } = useInView();
  const { ref: imageRef, isVisible: imageVisible } = useInView();

  return (
    <div className="w-full flex flex-col">
      <div className="h-screen w-full flex flex-col">
        <Header />
        <div className="bg-[url(/background_1.svg)] bg-cover bg-center flex-1 flex items-center justify-around px-10">
          <div
            ref={textRef}
            className={`text-ui-dark max-w-[600px] flex flex-col gap-y-6 transition-all duration-700 ease-out transform
              ${
                textVisible
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
          >
            <p className="font-bold text-4xl leading-snug">
              Your Personal Map to the IT World — Together with KIZAK
            </p>
            <p className="font-light text-3xl leading-snug">
              KIZAK — your AI mentor for personalized learning, task
              recommendations, and support on your IT journey.
            </p>
          </div>

          <div
            ref={imageRef}
            className={`transition-all duration-700 ease-out transform
              ${
                imageVisible
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
          >
            <Image
              width={280}
              height={280}
              src={"/capibara.svg"}
              alt={"capybara"}
            />
          </div>
        </div>
      </div>

      <InitialSection
        title={"Power features of our project"}
        cards={cardData1}
      />

      <div className="text-center text-white bg-[#111] py-20 px-6">
        <p className="text-2xl font-light max-w-3xl mx-auto">
          Climb the career ladder with a personalized roadmap, a dedicated
          mentor, and expert help building your dream resume — everything you
          need for professional growth!
        </p>
      </div>

      <InitialSection title={"How it works"} cards={cardData2} />

      <div className="text-center text-white bg-[#111] py-20 px-6">
        <p className="text-2xl font-light max-w-3xl mx-auto">
          Your journey starts today — and KIZAK is with you every step of the
          way.
        </p>
      </div>

      <footer className="bg-ui-dark py-10">
        <p className="text-center text-white text-lg font-extralight">
          © Made by KIZAK team
        </p>
      </footer>
    </div>
  );
}
