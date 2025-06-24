import { MainContent } from "@/shared/components/main/main-content";

interface Props {
  params: Promise<{
    user_id: string;
  }>;
}

export default async function Home({}: Props) {
  return (
    <div className="h-full">
      <MainContent />
    </div>
  );
}
