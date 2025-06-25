interface NodeLinkProps {
  from: { x: number; y: number };
  to: { x: number; y: number };
}

export const NodeLink = ({ from, to }: NodeLinkProps) => (
  <svg className="absolute w-full h-full top-0 left-0 pointer-events-none transition-all duration-200">
    <line
      x1={from.x}
      y1={from.y}
      x2={to.x}
      y2={to.y}
      stroke="#DDDDDD"
      strokeWidth="1.6"
    />
  </svg>
);
