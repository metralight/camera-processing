import React from "react";

const Point = ({ x, y, r, color}) => (
  <circle
    cx={x}
    cy={y}
    r={r ? r : 1}
    fill={color ? color : "darkRed"}
  />
);

export default Point;
