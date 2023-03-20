import React, { useEffect, useRef, useState } from "react"
import VideoControlNode from "./VideoControlNode"

export default function VideoControls(props){
    const {nodes, working, onNodeChange} = props
    
    return <div className="ui inline form" style={{marginTop:"15px"}}>
        {
            nodes.map(node => {
                return <VideoControlNode
                    key={node["name"]}
                    node={node}
                    working={working}
                    onNodeChange={onNodeChange}
                />
            })
        }
    </div>
}