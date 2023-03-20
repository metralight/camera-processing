import React, { useEffect, useRef, useState } from "react"

export default function VideoControlNode(props){
    const {node, working, onNodeChange} = props
    const [prevNode, setPrevNode] = useState(null)
    const [value, setValue] = useState("")

    if ((!prevNode && node) || (prevNode && prevNode.value != node.value)){
        setValue(node.value)
        setPrevNode(node)
    }

    function formatUnit(unit){
        if (!unit){
            return null
        }

        return "["+ unit + "]"
    }

    // typ number pres validacni funci a jen na blur
    // jinak select prepnout hned vyberem volby
    function onNumberBlur(){
        // if (node.type === "number"){
        if (value == undefined || value == null || value < node.min || value > node.max){
            alertify.error("Invalid value or out of range")
            setValue("")
            return
        }
        // }
        
        onNodeChange(node, parseFloat(value))
    }

    return <div className="inline field">
        <label>
            {node.display_name}&nbsp;
            {formatUnit(node.unit)}
        </label>
        {
            node.type === "number" ?
                <input type="number"
                    min={node.min}
                    max={node.max}
                    value={value}
                    disabled={working}
                    onChange={(event)=>{setValue(event.currentTarget.value)}} 
                    onBlur={onNumberBlur} 
                    onKeyDown={(event) => {if (event.key === "Enter"){event.currentTarget.blur()}}}
                />
                :
                <select
                    value={node.value}
                    disabled={working}
                    onChange={
                        (event)=>{
                            setValue(event.currentTarget.value)
                            onNodeChange(node, event.currentTarget.value)
                        }
                    }
                >
                    {
                        node.options.map(option => {
                            return <option value={option.numeric_value}>
                                {option.display_name}
                            </option>
                        })
                    }
                </select>
        }
    </div>
}