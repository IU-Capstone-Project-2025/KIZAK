import { useEffect, useState } from "react";
import { X } from "lucide-react";

const reasons = [
  { value: "too_easy", label: "Слишком лёгкий / ничего нового" },
  { value: "wrong_skills", label: "Навыки не соответствуют моей цели" },
  { value: "too_hard", label: "Слишком сложный" },
  { value: "bad_author", label: "Не нравится преподаватель" },
  { value: "unavailable", label: "Курс недоступен или устарел" },
];

interface Props {
  open: boolean;
  onClose: () => void;
  onSelect: (reason: string) => void;
}

export const DislikeReasonModal: React.FC<Props> = ({
  open,
  onClose,
  onSelect,
}) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (open) {
      setShow(true);
    } else {
      const timeout = setTimeout(() => setShow(false), 200);
      return () => clearTimeout(timeout);
    }
  }, [open]);

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center bg-black/40 transition-all duration-200 ${
        open ? "opacity-100 visible" : "opacity-0 invisible pointer-events-none"
      }`}
    >
      <div
        className={`bg-white rounded-lg p-6 w-full max-w-md shadow-lg relative transform transition-all duration-200 ${
          open ? "scale-100 opacity-100" : "scale-95 opacity-0"
        }`}
      >
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-black transition"
        >
          <X size={20} />
        </button>
        <h2 className="text-xl font-bold mb-4">Почему не понравился курс?</h2>
        <div className="space-y-2">
          {reasons.map((r) => (
            <button
              key={r.value}
              onClick={() => {
                onSelect(r.value);
                onClose();
              }}
              className="w-full text-left px-4 py-2 rounded-md border border-gray-200 hover:bg-gray-100 transition"
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
