import React, { useEffect, useRef } from "react";
import Line from "./Line"
import Point from "./Point";
import MotorHelper from "../../utils/MotorHelper";
import { STEP_TYPE_MOVE_LIN, STEP_TYPE_TOOL } from "../../constants/steps";

const ZERO_POINT_COLOR = "blue"

export default function ImageSvgView(props){
    const {config, image, onClick, ...rest} = props
    const ref = useRef()
    const refSvg = useRef()
    let svgEl = null

    useEffect(() => {
        svgEl = ref.current.querySelector("svg")
        if (svgEl){
            refSvg.current = svgEl
            svgEl.setAttribute("width", "400px")
            svgEl.setAttribute("height", "400px")
        }
    }, [image])

    function svgClick(reactEvent){
        const e = reactEvent.nativeEvent

        const pt = refSvg.current.createSVGPoint();
        
        // pass event coordinates
        pt.x = e.clientX;
        pt.y = e.clientY;
        
        // transform to SVG coordinates
        const svgP = pt.matrixTransform( refSvg.current.getScreenCTM().inverse() );
        
        // add or move zero circle SVG element
        // zeroOnSvg
        const NS = refSvg.current.getAttribute('xmlns');
        let circle = refSvg.current.querySelector(".zeroCircle")
        if (!circle){
            circle = document.createElementNS(NS, 'circle');
            circle.setAttribute('class', "zeroCircle");
            circle.setAttribute('cx', svgP.x);
            circle.setAttribute('cy', svgP.y);
            circle.setAttribute('r', 1);
            circle.setAttribute('fill', "red");
            refSvg.current.appendChild(circle);
        }else{
            circle.setAttribute('cx', svgP.x);
            circle.setAttribute('cy', svgP.y);
        }
        if (onClick){
            onClick({x : svgP.x, y : svgP.y})
        }
        
    }
    
    return <div  ref={ref} dangerouslySetInnerHTML={{__html : image}}  onClick={svgClick}>

        
    </div>
}