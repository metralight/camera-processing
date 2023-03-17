import React, { useEffect, useRef, useState } from "react"
import VideoControlNode from "./VideoControlNode"

export default function VideoControls(props){
    const {nodes, onNodeChange} = props
    
    return <div className="ui inline form" style={{marginTop:"15px"}}>
        {
            nodes.map(node => {
                return <VideoControlNode node={node} onNodeChange={onNodeChange} />
            })
        }
    </div>
}