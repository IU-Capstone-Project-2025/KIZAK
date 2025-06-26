import React from "react";

interface Props {
  className?: string;
  progress: number;
  size?: number;
  strokeWidth?: number;
  bgColor?: string;
}

function getColor(progress: number) {
  if (progress >= 70) {
    return "#3F9965";
  } else if (progress >= 50) {
    return "#D0B16C";
  } else {
    return "#993F3F";
  }
}

export const ProgressCircle: React.FC<Props> = ({
  className = "",
  progress,
  size = 48,
  strokeWidth = 6,
  bgColor = "#E5E7EB",
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - progress / 100);

  return (
    <svg
      width={size}
      height={size}
      className={className}
      viewBox={`0 0 ${size} ${size}`}
    >
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={bgColor}
        strokeWidth={strokeWidth}
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={getColor(progress)}
        strokeWidth={strokeWidth}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(180 ${size / 2} ${
          size / 2
        }) scale(-1 1) translate(-${size} 0)`}
        strokeLinecap="round"
      />
      <text
        x="50%"
        y="52%"
        fill={"#1f1f1f"}
        fontSize={size * 0.25}
        fontWeight="medium"
        textAnchor="middle"
        dominantBaseline="middle"
      >
        {Math.round(progress)}%
      </text>
    </svg>
  );
};
