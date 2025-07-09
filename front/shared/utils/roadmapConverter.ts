type RawNode = {
  node_id: string;
  title: string;
  summary: string;
};

type RawLink = {
  from_node: string;
  to_node: string;
};

type Node = {
  node_id: string;
  progress: Progress;
  resource_id: string;
  roadmap_id: string;
  summary: string;
  title: string;
};

type Link = {
  from_node: string;
  link_id: string;
  roadmap_id: string;
  to_node: string;
};

type RoadmapInfo = {
  roadmap_id: string;
  nodes: Node[];
  links: Link[];
};

type Progress = "Done" | "In progress" | "Not started";

export async function fetchRoadmapData(userId: string): Promise<{
  rawNodes: RawNode[];
  rawLinks: RawLink[];
  initialProgress: Record<string, Progress>;
}> {
  try {
    const response = await fetch(
      `http://localhost:8000/roadmap_by_user_id/${userId}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const roadmapInfo: RoadmapInfo = await response.json();

    const rawNodes: RawNode[] = roadmapInfo.nodes.map((node) => ({
      node_id: node.node_id,
      title: node.title,
      summary: node.summary,
    }));

    const rawLinks: RawLink[] = roadmapInfo.links.map((link) => ({
      from_node: link.from_node,
      to_node: link.to_node,
    }));

    const initialProgress: Record<string, Progress> = {};
    roadmapInfo.nodes.forEach((node) => {
      if (isValidProgress(node.progress)) {
        initialProgress[node.node_id] = node.progress;
      } else {
        console.warn(
          `Invalid progress value for node ${node.node_id}: ${node.progress}`
        );
        initialProgress[node.node_id] = "Not started";
      }
    });

    return { rawNodes, rawLinks, initialProgress };
  } catch (error) {
    console.error("Error fetching roadmap data:", error);
    throw error;
  }
}

function isValidProgress(value: string): value is Progress {
  return ["Done", "In progress", "Not started"].includes(value);
}
