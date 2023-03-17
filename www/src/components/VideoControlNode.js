import React, { useEffect, useRef, useState } from "react"

export default function VideoControlNode(props){
    const {node, onNodeChange} = props
    
    function formatUnit(unit){
        if (!unit){
            return null
        }

        return "["+ unit + "]"
    }
    return <div className="inline field">
        <label>
            {node.display_name}&nbsp;
            {formatUnit(node.unit)}
        </label>
        {
            node.type === "number" ?
                <input type="number" min={node.min} max={node.max} value={node.value} />
                :
                <select value={node.value}>
                    {
                        node.options.map(option => {
                            return <option>
                                {option.display_name}
                            </option>
                        })
                    }
                </select>
        }
    </div>
}