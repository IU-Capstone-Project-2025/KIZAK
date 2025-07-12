"use client";

import { useEffect, useState } from "react";
import { CustomSelect } from "./select";
import { Progress } from "./node";
import { ThumbsDown, ThumbsUp, X } from "lucide-react";
import { DislikeReasonModal } from "./DislikeReasonModal";
import { API_BASE_URL } from "@/shared/types/types";

type ResourceResponse = {
  resource_type: string;
  title: string;
  summary: string;
  content: string;
  level: string;
  price: number;
  language: string;
  duration_hours: number;
  platform: string;
  rating: number;
  published_date: string;
  certificate_available: boolean;
  skills_covered: string[];
  resource_id: string;
};

interface Props {
  resourceId: string;
  onClose: () => void;
  progress: string;
  onProgressChange: (newProgress: string) => void;
  node_id: string;
  roadmap_id: string;
  user_id: string;
}

export const ResourceDetails: React.FC<Props> = ({
  resourceId,
  onClose,
  progress,
  onProgressChange,
  roadmap_id,
  user_id,
  node_id,
}) => {
  const [resource, setResource] = useState<ResourceResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDislikeModal, setShowDislikeModal] = useState(false);
  const [isDisliked, setIsDisliked] = useState(false);

  const handleDislikeReason = async (reason: string) => {
    try {
      await fetch(`${API_BASE_URL}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user_id,
          roadmap_id: roadmap_id,
          node_id: node_id,
          resource_id: resourceId,
          is_liked: false,
          reason,
        }),
      });
      setIsDisliked(true);
    } catch (e) {
      console.error("Ошибка при отправке фидбека", e);
    }
  };

  useEffect(() => {
    const fetchResource = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/resources/${resourceId}`);
        if (!res.ok) throw new Error("Failed to fetch resource");
        const data = await res.json();
        setResource(data);
      } catch (err) {
        setError("Ошибка загрузки ресурса");
      } finally {
        setLoading(false);
      }
    };

    fetchResource();
  }, [resourceId]);

  if (loading) return <div className="p-6">Загрузка...</div>;
  if (error || !resource)
    return (
      <div
        className="relative flex flex-col h-full p-6 rounded-md shadow-md overflow-auto
        bg-bg-main text-ui-dark border border-ui-border"
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-8 h-8 flex-center rounded-full
          text-ui-muted hover:text-ui-dark transition"
        >
          <X size={20} />
        </button>
      </div>
    );

  return (
    <div
      className="relative flex flex-col h-full p-6 rounded-md shadow-md overflow-auto
        bg-bg-main text-ui-dark border border-ui-border"
    >
      <button
        onClick={onClose}
        className="absolute top-4 right-4 w-8 h-8 flex-center rounded-full
          text-ui-muted hover:text-ui-dark transition"
        title="Закрыть"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-5 h-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>

      <div className="text-3xl font-extrabold mb-4 flex-center gap-x-3 text-brand-primary">
        {resource.title}
        <button
          onClick={() => setShowDislikeModal(true)}
          className="w-8 h-8 flex-center text-red-500 hover:text-red-700 transition"
        >
          <ThumbsDown size={24} />
        </button>
        <DislikeReasonModal
          open={showDislikeModal}
          onClose={() => setShowDislikeModal(false)}
          onSelect={handleDislikeReason}
        />
      </div>
      <p className="mb-4 text-lg leading-relaxed">{resource.summary}</p>

      <label htmlFor="progress-select" className="block font-semibold mb-2">
        Прогресс
      </label>
      <CustomSelect
        className="mb-4"
        options={["Not started", "In progress", "Done"]}
        value={progress as Progress}
        onChange={onProgressChange}
      />

      <a
        href={resource.content}
        target="_blank"
        rel="noopener noreferrer"
        className="mb-6 w-fit text-brand-primary underline hover:text-yellow-400 transition"
      >
        Перейти к курсу
      </a>

      <div className="grid grid-cols-2 gap-x-12 gap-y-4 text-ui-dark text-sm font-semibold">
        <div className="flex-between">
          <span className="text-ui-muted">Уровень:</span>
          <span>{resource.level}</span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Цена:</span>
          <span>
            {resource.price === 0 ? "Бесплатно" : `${resource.price} ₽`}
          </span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Язык:</span>
          <span>{resource.language}</span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Длительность:</span>
          <span>{resource.duration_hours} ч.</span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Платформа:</span>
          <span>{resource.platform}</span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Рейтинг:</span>
          <span>{resource.rating}</span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Дата публикации:</span>
          <span>{resource.published_date}</span>
        </div>
        <div className="flex-between">
          <span className="text-ui-muted">Сертификат:</span>
          <span
            className={
              resource.certificate_available ? "text-status-success" : ""
            }
          >
            {resource.certificate_available ? "Доступен" : "Нет"}
          </span>
        </div>
        <div className="col-span-2 mt-4">
          <span className="text-ui-muted font-semibold mb-2">
            Изучаемые навыки:
          </span>
          <div className="mt-1 flex flex-wrap gap-2">
            {resource.skills_covered.map((skill) => (
              <span
                key={skill}
                className="px-2 py-1 rounded shadow-sm font-medium border border-ui-border text-ui-dark"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
