import React, { useEffect, useRef, useState } from "react"
import Loader from "./Loader"
import { io } from "socket.io-client"
import { startCapture, stopCapture, getDevices, getConfig } from "../apiFunctions"
import Overview from "./Overview"
import ErrorBoundary from "./ErrorBoundary"
import TopMenu from "./TopMenu"


const socket = io();
socket.on("SOCKET_IO_ERROR", (e) => {
    alertify.error("Socket IO error: " + e)
})

export default function App(props){
    const [config, setConfig] = useState(null)
    const [devices, setDevices] = useState(null)
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
        startCapture(socket, device).then(()=>{
            setWorking(false)
            setCapturing(true)
        }).catch((err) => {
            alertify.error("Can not start capture: " + err)
            console.log(err)
            setWorking(false)
            setCapturing(false)
        })
    }

    function onStopCaputure(device){
        setWorking(true)
        stopCapture(socket).then(()=>{
            setWorking(false)
            setCapturing(false)
        }).catch((err) => {
            alertify.error("Can not stop capture: " + err)
            console.log(err)
            setWorking(false)
            setCapturing(false)
        })
    }

    if (!config){
        return <Loader text="Loading data" />
    }

    return <div>
        <ErrorBoundary>
            <TopMenu 
                devices={devices}
                onStartCaputure={onStartCaputure}
                working={working}
                capturing={capturing}
                onStopCapture={onStopCaputure}
            />
        </ErrorBoundary>
        <div className="ui grid">
            <div className="sixteen wide column">
                <ErrorBoundary>
                    {
                        capturing ? 
                            <Overview config={config} io={socket} />
                            :
                            null
                    }                    
                </ErrorBoundary>
            </div>
        </div>
    </div>
}