import { useState, useRef, useEffect } from "react";
import { Progress } from "./node";

interface CustomSelectProps {
  options: Progress[];
  value: Progress;
  onChange: (val: Progress) => void;
  className?: string;
}

export const CustomSelect: React.FC<CustomSelectProps> = ({
  options,
  value,
  onChange,
  className,
}) => {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className={`relative ${className}`} ref={ref}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full p-2 border border-ui-border rounded bg-white text-ui-dark flex justify-between items-center hover:border-ui-muted transition-colors"
      >
        <span>{value}</span>
        <svg
          className={`w-5 h-5 text-ui-muted transition-transform duration-200 ${
            open ? "rotate-180" : ""
          }`}
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <ul
        className={`absolute left-0 right-0 mt-1 max-h-40 overflow-auto rounded border border-ui-border bg-white shadow-md z-20
          transition-all duration-200 ease-in-out origin-top
          ${
            open
              ? "opacity-100 scale-100"
              : "opacity-0 scale-95 pointer-events-none"
          }
        `}
      >
        {options.map((option) => (
          <li
            key={option}
            onClick={() => {
              onChange(option);
              setOpen(false);
            }}
            className={`cursor-pointer px-4 py-2 transition-all duration-300
              ${option === value ? "bg-bg-subtle/70 font-semibold" : ""}
            `}
          >
            {option}
          </li>
        ))}
      </ul>
    </div>
  );
};
