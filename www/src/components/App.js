import React, { useEffect, useRef, useState } from "react"
import Loader from "./Loader"
import { io } from "socket.io-client"
import { startCapture, stopCapture, getDevices, getConfig, updateNode } from "../apiFunctions"
import Video from "./Video"
import VideoControls from "./VideoControls"
import ErrorBoundary from "./ErrorBoundary"
import CameraConnect from "./CameraConnect"


const socket = io();
socket.on("SOCKET_IO_ERROR", (e) => {
    alertify.error("Socket IO error: " + e)
})

export default function App(props){
    const [config, setConfig] = useState(null)
    const [devices, setDevices] = useState(null)
    const [controlNodes, setControlNodes] = useState(null)
    const [working, setWorking] = useState(null)
    const [capturing, setCapturing] = useState(null)

    useEffect(() => {
        getDevices(socket).then((devices) => {
            setDevices(devices)
        }).catch((data) => {
            console.error(data)
            alertify.error("Error while getting devies list")
        }) 

        getConfig(socket).then((config) => {
            setConfig(config)
        }).catch((data) => {
            console.error(data)
            alertify.error("Error while getting config")
        })  
        
    }, [])
    
    function onStartCaputure(device){
        setWorking(true)
        startCapture(socket, device).then((controlNodes)=>{
            setWorking(false)
            setCapturing(true)
            setControlNodes(controlNodes)
        }).catch((err) => {
            alertify.error("Can not start capture: " + err)
            console.log(err)
            setWorking(false)
            setCapturing(false)
            setControlNodes(null)
        })
    }

    function onStopCaputure(device){
        setWorking(true)
        stopCapture(socket).then(()=>{
            setWorking(false)
            setCapturing(false)
            setControlNodes(null)
        }).catch((err) => {
            alertify.error("Can not stop capture: " + err)
            console.log(err)
            setWorking(false)
            setCapturing(false)
            setControlNodes(null)
        })
    }

    function onNodeChange(node, value){
        setWorking(true)
        updateNode(socket, node, value).then((nodes)=>{
            setWorking(false)
            setControlNodes(nodes)
        }).catch((err) => {
            alertify.error("Can not update value: " + err)
            console.log(err)
            setWorking(false)
        })
    }

    if (!config){
        return <Loader text="Loading data" />
    }

    return <div>
       
        <div className="ui grid">
            <div className="row">
                <div className="three wide column">
                    <div className="ui message">
                        <ErrorBoundary>
                            <CameraConnect 
                                devices={devices}
                                onStartCaputure={onStartCaputure}
                                working={working}
                                capturing={capturing}
                                onStopCapture={onStopCaputure}
                            />
                        </ErrorBoundary>
                        <ErrorBoundary>
                            {
                                (capturing && controlNodes) ? 
                                    <VideoControls
                                        nodes={controlNodes}
                                        working={working}
                                        onNodeChange={onNodeChange}
                                    />
                                    :
                                    null
                            }
                        </ErrorBoundary>
                    </div>
                </div>

                <div className="thirteen wide column">
                    <div className="ui grid">
                        <div className="sixteen wide column">
                            {   capturing ? 
                                    <div>
                                        <img src="/main" />
                                    </div>
                                    :
                                    null
                            }
                        </div>
                        <div className="nine wide column">
                            <h3>Horizontal centroid</h3>
                            {   capturing ? 
                                    <div>
                                        <img src="/cut_horizontal" />
                                    </div>
                                    :
                                    null
                            }
                        </div>
                        <div className="seven wide column">
                            <h3>Vertical centroid</h3>
                            {   capturing ?
                                    <img src="/cut_vertical" />
                                    :
                                    null
                            }
                        </div>
                    </div>
                    
                </div>

                
            </div>

            <div className="row">
                <div className="eight wide column"></div>
            </div>
        </div>
    </div>
}