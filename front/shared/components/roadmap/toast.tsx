import { RefreshCw } from "lucide-react";

interface FeedbackToastProps {
  show: boolean;
}

export const FeedbackToast: React.FC<FeedbackToastProps> = ({ show }) => {
  return (
    <div
      className={`fixed bottom-6 right-6 max-w-xs w-[300px] bg-white shadow-lg rounded-xl border border-ui-border p-4 flex items-start gap-3 transition-transform duration-500 ease-out
      ${show ? "translate-x-0 opacity-100" : "translate-x-full opacity-0"}`}
    >
      <div className="flex flex-col text-ui-dark">
        <span className="font-semibold text-lg mb-1">Спасибо за отзыв!</span>
        <p className="text-sm">
          Хотите изменить родмап? В сайдбаре есть кнопка{" "}
          <RefreshCw
            width={22}
            height={22}
            strokeWidth={1.8}
            className="inline-block text-brand-primary"
          />{" "}
          для переделки.
        </p>
      </div>
    </div>
  );
};
