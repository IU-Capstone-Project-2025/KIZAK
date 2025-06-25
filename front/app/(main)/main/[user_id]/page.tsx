import { MainContent } from "@/shared/components/main/content";

interface Props {
  params: {
    user_id: string;
  };
}

export default function Home({ params }: Props) {
  return (
    <div className="h-full">
      <MainContent userId={params.user_id} />
    </div>
  );
}
