import React, { useEffect, useRef, useState } from "react"
import Loader from "./Loader"
import { io } from "socket.io-client"
import { startCapture, stopCapture, getDevices, getConfig, updateNode, getMeasData, getInitState } from "../apiFunctions"
import Video from "./Video"
import VideoControls from "./VideoControls"
import ErrorBoundary from "./ErrorBoundary"
import CameraConnect from "./CameraConnect"
import MeasData from "./MeasData"


const socket = io();
socket.on("SOCKET_IO_ERROR", (e) => {
    alertify.error("Socket IO error: " + e)
})

export default function App(props){
    const [config, setConfig] = useState(null)
    const [devices, setDevices] = useState(null)
    const [controlNodes, setControlNodes] = useState(null)
    const [working, setWorking] = useState(false)
    const [capturing, setCapturing] = useState(false)
    const capturingRef = useRef(false)
    const [measuringData, setMeasuringData] = useState(null)

    useEffect(() => {
        capturingRef.current = capturing
    }, [capturing])

    useEffect(() => {
        getConfig(socket).then((config) => {
            setConfig(config)
        }).catch((data) => {
            console.error(data)
            alertify.error("Error while getting config")
        })  

        getInitState(socket).then((state) => {
            setCapturing(state.capturing)
            setDevices(state.devices)
            if (state.capturing){
                setControlNodes(state.nodes)
                getMeasuringDataStream()
            }
        }).catch((data) => {
            console.error(data)
            alertify.error("Error while getting app state")
        })        
        
    }, [])

    function getMeasuringDataStream(){
        getMeasData(socket).then((data) => {
            console.log(data)
            setMeasuringData(data)
        }).catch((data) => {
            console.error(data)
            alertify.error("Error while getting measuring data")
        }).finally(() => {
            setTimeout(() => {
                if (capturingRef.current){
                    getMeasuringDataStream()
                }
            }, 20)
        })
    }
    
    function onStartCaputure(device){
        setWorking(true)
        startCapture(socket, device).then((controlNodes)=>{
            setCapturing(true)
            setControlNodes(controlNodes)
            getMeasuringDataStream()
        }).catch((err) => {
            alertify.error("Can not start capture: " + err)
            console.log(err)
            setCapturing(false)
            setControlNodes(null)
        }).finally(() => {
            setWorking(false)
        })
    }

    function onStopCaputure(device){
        setWorking(true)
        stopCapture(socket).then(()=>{
            setCapturing(false)
            setControlNodes(null)
            setMeasuringData(null)
        }).catch((err) => {
            alertify.error("Can not stop capture: " + err)
            console.log(err)
        }).finally(() => {
            setWorking(false)
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

                    {
                        (capturing && measuringData) && <MeasData data={measuringData} />
                    }
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
                            {   capturing ? 
                                    <React.Fragment>
                                        <h3>Horizontal centroid</h3>
                                        <img src="/cut_horizontal" />
                                    </React.Fragment>
                                    :
                                    null
                            }
                        </div>
                        <div className="seven wide column">
                            {   capturing ?
                                    <React.Fragment>
                                        <h3>Vertical centroid</h3>
                                        <img src="/cut_vertical" />
                                    </React.Fragment>
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