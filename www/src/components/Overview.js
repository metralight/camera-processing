import React, { useEffect, useRef, useState } from "react"
import Loader from "./Loader"
import Modal from "./Modal"


export default function Overview(props){
    const { io, config } = props
    const [image, setImage] = useState(null)
    const [workingStatus, setWorkingStatus] = useState(null)

    // useEffect(() => {
    //     io.on(EVENT_IMAGE, ImageReceived)
    //     return () => {
    //         io.off(EVENT_IMAGE, ImageReceived)
    //     }
    // }, [])
    
    
    if (!config){
        return <Loader text="Loading data" />
    }

    return <div className="ui grid">
        {
            workingStatus && <Loader text={workingStatus}></Loader>
        }
        <div className="row">
            <div className="four wide column"></div>
            <div className="twelve wide column">
                <img src="/video" />
            </div>
        </div>       
    </div>
}