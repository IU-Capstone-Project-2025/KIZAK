import { MainContent } from "@/shared/components/main/content";

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
