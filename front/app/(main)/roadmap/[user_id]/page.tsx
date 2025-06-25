import { RoadmapNew } from "@/shared/components/roadmap/roadmap-new";

interface Props {
  params: {
    user_id: string;
  };
}

export default function RoadmapPage({ params }: Props) {
  return (
    <section
      className={`flex flex-col w-full h-full rounded-xl group border shadow-sm border-ui-border`}
    >
      <h2 className="text-ui-dark text-start text-lg w-full pl-3 py-1 border-b border-ui-border">
        Roadmap
      </h2>
      <div className="flex-1 w-full relative">
        <RoadmapNew userId={params.user_id} />
      </div>
    </section>
  );
}
