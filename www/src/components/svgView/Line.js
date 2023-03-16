import React from "react";

export default function Line({x1, x2, y1, y2, stroke, color}){
    return <g>
        <line
            x1={x1}
            y1={y1}
            x2={x2}
            y2={y2}
            stroke={color ? color : "red"}
            strokeWidth={stroke ? stroke : 0.5}
        />
        {/* <line
            x1={corner1.x}
            y1={corner1.y}
            x2={corner2.x}
            y2={corner2.y}
            stroke=" rgba(8, 16, 128, 0.9)"
            strokeWidth={thickness / 2}
            strokeDasharray={`${thickness * 3} ${thickness}`}
        /> */}
  </g>
}