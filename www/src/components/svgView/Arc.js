import React from "react";

const degrees_to_radians = function (degrees)
{
  var pi = Math.PI;
  return degrees * (pi/180);
}

const radians_to_degrees = function (radians)
{
  var pi = Math.PI;
  return (radians * 180) / pi
}



const Arc = ({ start, center, angle, direction, color, stroke}) => {
    const radius = Math.sqrt(Math.pow(start.x - center.x, 2) + Math.pow(start.y - center.y, 2))

    //uhel se zadava absolutne na kruhu
    //pro ucel vykresleni se musi prepocitat
    // const startCenterAngle = 90 - radians_to_degrees(Math.atan((center.x - start.x) / (center.y - start.y)))
    
    const largeArcFlag = Number(Math.abs(angle) > 180)
    const sweepFlag = Number(angle > 0)
    
    //rotate point to get target
    const s = Math.sin(degrees_to_radians(angle))
    const c = Math.cos(degrees_to_radians(angle))
    // const targetPoint = {
    //     x: start.x,
    //     y: start.y,
    // }
    // targetPoint.x -= center.x
    // targetPoint.y -= center.y
    // const xnew = ;
    // const ynew = ;
    const targetPoint = {
        x : (start.x - center.x) * c - (start.y - center.y) * s + center.x,
        y : (start.x - center.x) * s + (start.y - center.y) * c + center.y
    }

    // sestavit string
    let dataStr = `M ${start.x} ${start.y} `
    dataStr+= `A ${radius} ${radius} 0 ${largeArcFlag} ${sweepFlag} ${targetPoint.x} ${targetPoint.y} `

    return <path
        d={dataStr}
        stroke={color ? color : "red"}
        strokeWidth={stroke ? stroke : 0.5}
        fill="none"
    />
};

export default Arc;
