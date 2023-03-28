import React, { useEffect, useRef, useState } from "react"

export default function CameraConnect(props){
    const {devices, onStartCaputure, working, capturing, onStopCapture} = props
    const [selectedDevice, setSelectedDevice] = useState(null)
    const [prevDevices, setPrevDevices] = useState(null)
    const dropdownEl = useRef(null);

    // pri nacteni kde uz jsou vyctene devices dat do selectedDevice prvni kameru
    // prvni nacteni devices pozname pomoci prevDevices
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
        setSelectedDevice({"model" : device.model, "serial_number" : device.serial_number})
    }
    
    // return <div className="ui stackable top attached inverted menu">
    //     <div className="item">
    //         <select
    //             className="ui dropdown"
    //             value={selectedDevice ? selectedDevice.model : ""}
    //             onChange={onChangeDevice} 
    //             ref={dropdownEl}
    //         >
    //             {(devices ? devices : []).map((dev) => {
    //                 return <option value={dev.model} key={dev.model}>
    //                     {dev.model}
    //                 </option>
    //             })}
    //         </select>
    //         &nbsp;
    //         <button className="ui button" disabled={working} onClick={onStartStopClick}>
    //             <i className={(capturing ? "stop icon" : "play icon")} />
    //             {(capturing ? "Stop capture" : "Start capture")}
    //         </button>
    //     </div>
    // </div>
    return <div className="ui form">
            <select
                className="ui dropdown"
                value={selectedDevice ? selectedDevice.model : ""}
                onChange={onChangeDevice} 
                ref={dropdownEl}
            >
                {(devices ? devices : []).map((dev) => {
                    return <option value={dev.model} key={dev.model} disabled={dev.access_status !== "READY"}>
                        {dev.model} [{dev.access_status}]
                    </option>
                })}
            </select>
            &nbsp;
            <button className="ui icon button" disabled={working} onClick={onStartStopClick}>
                <i className={(capturing ? "stop icon" : "play icon")} />
                {/* {(capturing ? "Stop" : "Start")} */}
            </button>
        </div>
}