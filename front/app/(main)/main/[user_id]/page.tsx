import { MainContent } from "@/shared/components/main/content";

interface PageProps {
  params: Promise<{ user_id: string }>;
}

export default async function Home({ params }: PageProps) {
  const { user_id } = await params;
  return (
    <div className="h-full">
      <MainContent userId={user_id} />
    </div>
  );
}
