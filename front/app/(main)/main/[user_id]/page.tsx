import { MainContent } from "@/shared/components/main/main-content";

interface Props {
  params: Promise<{
    user_id: string;
  }>;
}

export default async function Home({ params }: Props) {
  const userInfo = await params;

  return (
    <div className="h-full">
      <MainContent />
    </div>
  );
}
