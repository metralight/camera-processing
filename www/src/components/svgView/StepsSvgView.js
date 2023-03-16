import React from "react";
import Point from "./Point";
import { STEP_TYPE_MOVE_ARC_CW, STEP_TYPE_MOVE_ARC_CCW, STEP_TYPE_MOVE_CIRC_CW, STEP_TYPE_MOVE_CIRC_CCW, STEP_TYPE_MOVE_LIN, STEP_TYPE_TOOL } from "../../constants/steps";

const TOOL_STEP_COLOR = "green"
const HOVER_STEP_COLOR = "magenta"
const MOVE_STEP_COLOR = "darkRed"
const CURRENT_POSITION_COLOR = "blue"
const LINE_COLOR = "red"
const HOVER_RADIUS_MULT = 2

const degrees_to_radians = function (degrees)
{
  var pi = Math.PI;
  return degrees * (pi/180);
}


const ArcStr = function(prevStep, step){
    const radius = Math.sqrt(Math.pow(step.centerOffsetX, 2) + Math.pow(step.centerOffsetY, 2))
    const sweepFlag = step.moveType === STEP_TYPE_MOVE_ARC_CW ? 1 : 0
    
    const centerX = prevStep.x + step.centerOffsetX
    const centerY = prevStep.y + step.centerOffsetY
    
    const vecX = prevStep.x - step.x
    const vecY = prevStep.y - step.y

    const lineA = vecY
    const lineB = -vecX
    const lineC = -(lineA * step.x + lineB * step.y)
    
	const dist = (lineA*centerX + lineB*centerY + lineC)/Math.sqrt(lineA*lineA + lineB*lineB)
    const largeArcFlag = ((dist < 0 && step.moveType === STEP_TYPE_MOVE_ARC_CW) || (dist > 0 && step.moveType === STEP_TYPE_MOVE_ARC_CCW)) ? 1 : 0
    
    // sestavit string
    let dataStr = `M ${prevStep.x} ${prevStep.y} `
    dataStr+= ` A ${radius} ${radius} 0 ${largeArcFlag} ${sweepFlag} ${step.x} ${step.y} `
    return dataStr
}

const CircStr = function(step){
    const radius = Math.sqrt(Math.pow(step.centerOffsetX, 2) + Math.pow(step.centerOffsetY, 2))
    const largeArcFlag = 1
    const sweepFlag = 1
        
    
    // cilovy bod nesmi byt v svg stejny - posuneme o setinku a pak to doplnime linearem
    //rotate point to get target
    const s = Math.sin(degrees_to_radians(359))
    const c = Math.cos(degrees_to_radians(359))
    const targetPoint = {
        x : (-step.centerOffsetX * c) - (-step.centerOffsetY * s) + step.x + step.centerOffsetX,
        y : (-step.centerOffsetX * s) + (-step.centerOffsetY * c) + step.y + step.centerOffsetY
    }

    // sestavit string
    let dataStr = `M ${step.x} ${step.y} `
    dataStr+= ` A ${radius} ${radius} 0 ${largeArcFlag} ${sweepFlag} ${targetPoint.x} ${targetPoint.y} `
    dataStr+= ` L ${step.x} ${step.y} `
    return dataStr
}

export default function StepsSvgView(props){
    const {config, hoveredStepKey, style} = props
    let { steps, position } = props
    let w, h, viewBox;

    // vypocitat minimum v x a y a podle toho nastavit viewport
    const minX = Math.min(...steps.map(step => step.x ), position.x)
    // const minY = Math.min(...steps.map(step => step.y ), position.y)
    const minY = 200
    const maxX = Math.max(...steps.map(step => step.x ), position.x)
    const maxY = Math.max(...steps.map(step => step.y ), position.y)
    const offsetW = 5
    const offsetH = 5
    w = maxX-minX+offsetW
    h = maxY-minY+offsetH
    viewBox = `${minX-offsetW/2} ${minY-offsetH/2} ${w} ${h}`

    // parametry prvku
    const lineStroke = w / 200
    const pointRadius = w / 120
    const toolPointRadius = w / 100

    //ukladat pri prochazeni body kde se meni tools
    const toolPointsPosition = []

    // prochazet body a sestavovat trajektorii
    let lastPosition = null     
    let dataStr = ""
    for (let index = 0; index < steps.length; index++) {
        const step = steps[index]

        if (index == 0){
            dataStr += ` M ${step.x} ${step.y} `
            lastPosition = step
            continue
        }

        // ukladat pozice tools
        if (step.type === STEP_TYPE_TOOL) {
            if (lastPosition){
                toolPointsPosition.push({
                    x : lastPosition.x,
                    y : lastPosition.y, 
                })
            }
        }
        
        // pridavat do path caru/krivku podle toho co je to za krok
        if (step.moveType === STEP_TYPE_MOVE_LIN) {
            dataStr += `L ${step.x} ${step.y} `
            lastPosition = step
        }else if (step.moveType === STEP_TYPE_MOVE_ARC_CW || step.moveType === STEP_TYPE_MOVE_ARC_CCW) {
            dataStr += ArcStr(lastPosition, step)
            lastPosition = step
        }else if (step.moveType === STEP_TYPE_MOVE_CIRC_CW || step.moveType === STEP_TYPE_MOVE_CIRC_CCW) {
            dataStr += CircStr(step)
            //nemenit last position protoze po kruhovem pohybu jsme stale ve stejnem bode !
        }
        
    }
    

    return <svg viewBox={viewBox} {...style} >
        <path d={dataStr} stroke={LINE_COLOR} strokeWidth={lineStroke} fill="none" />
        {/* {
            stepDoubles.map(([step1, step2]) => (
                <Line
                    x1={step1.x}
                    y1={step1.y}
                    x2={step2.x}
                    y2={step2.y}
                    stroke={lineStroke}
                    color={LINE_COLOR}
                />
            ))
        } */}
        {
            steps.map(step => (
                <Point
                    x={step.x}
                    y={step.y}
                    r={step.key === hoveredStepKey ? pointRadius * HOVER_RADIUS_MULT : pointRadius }
                    color={step.key === hoveredStepKey ? HOVER_STEP_COLOR : MOVE_STEP_COLOR}  
                />
            ))
        }
        {
            toolPointsPosition.map(step => (
                <Point
                    x={step.x}
                    y={step.y}
                    r={step.key === hoveredStepKey ? toolPointRadius * HOVER_RADIUS_MULT : toolPointRadius  }
                    color={step.key === hoveredStepKey ? HOVER_STEP_COLOR : TOOL_STEP_COLOR }  
                />
            ))
        }

        <Point
            x={position.x}
            y={position.y}
            r={pointRadius}
            color={CURRENT_POSITION_COLOR}  
        />
    </svg>
}