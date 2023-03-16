import React, { useEffect, useRef, useState } from "react"

export default function TopMenu(props){
    const {devices, onStartCaputure, working, capturing, onStopCapture} = props
    const [selectedDevice, setSelectedDevice] = useState(null)
    const [prevDevices, setPrevDevices] = useState(null)
    const dropdownEl = useRef(null);

    // pri prvnim nacteni dat do selectedDevice prvni kameru
    if (devices && devices.length && prevDevices==null){
        setSelectedDevice(devices[0])
        setPrevDevices(devices)
    }

    useEffect(() => {
        $(dropdownEl.current).dropdown()
    }, [])

    function onStartStopClick(){
        if (capturing){
            stopCapture()
        }else{
            startCapture()
        }
    }

    function stopCapture(){
        if (!capturing){
            alertify.warning("Calling stop capture when not capturing")
            return
        }
        onStopCapture()
    }

    function startCapture(){
        if (!selectedDevice){
            alertify.error("No selected device")
            return
        }
        onStartCaputure(selectedDevice)
    }

    function onChangeDevice(event){
        const selectedModel = event.currentTarget.value
        const device = devices.find(val => val.model===selectedModel)
        setSelectedDevice(device)
    }

    
    return <div className="ui stackable attached inverted menu">
        <div className="item">
            <select
                className="ui dropdown"
                value={selectedDevice ? selectedDevice.model : ""}
                onChange={onChangeDevice} 
                ref={dropdownEl}
            >
                {(devices ? devices : []).map((dev) => {
                    return <option value={dev.model} key={dev.model}>
                        {dev.model}
                    </option>
                })}
            </select>
            &nbsp;
            <button className="ui button" disabled={working} onClick={onStartStopClick}>
                <i className={(capturing ? "stop icon" : "play icon")} />
                {(capturing ? "Stop capture" : "Start capture")}
            </button>
        </div>
    </div>
}