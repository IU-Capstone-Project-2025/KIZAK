import { Header } from "@/shared/components/initial/header";
import { InitialSection } from "@/shared/components/initial/initial-section";
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

  return (
    <div className="w-full flex flex-col">
      <div className="h-screen w-full flex flex-col">
        <Header />
        <div className="bg-[url(/background_1.svg)] bg-cover bg-center flex-1 flex-center">
          <div className="text-ui-dark w-200 flex flex-col gap-y-4">
            <p className="font-bold text-4xl">
              Your Personal Map to the IT World — Together with KIZAK
            </p>
            <p className="font-light text-3xl">
              KIZAK — your AI mentor for personalized learning, task
              recommendations, and support on your IT journey.
            </p>
          </div>
          <Image
            width={280}
            height={280}
            src={"/capibara.svg"}
            alt={"capybara"}
          />
        </div>
      </div>
      <InitialSection
        title={"Power features of our project"}
        cards={cardData1}
      />
      <p className="text-center text-2xl font-extralight flex-center h-[300px] w-[70%] mx-auto">
        Climb the career ladder with a personalized roadmap, a dedicated mentor,
        and expert help building your dream resume — everything you need for
        professional growth!
      </p>
      <InitialSection title={"How it works"} cards={cardData2} />
      <p className="text-center text-2xl font-extralight flex-center h-[300px] w-[70%] mx-auto">
        Your journey starts today — and KIZAK is with you every step of the way
      </p>
      <footer className="text-center text-2xl font-extralight flex-center h-[200px] bg-ui-dark w-full">
        <p className="text-white">© Made by KIZAK team</p>
      </footer>
    </div>
  );
}
