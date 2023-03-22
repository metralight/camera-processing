// import {RELATIVE_MOVE} from "../../messageConstants.json"

function actionCreator(socket, msgConstant, emitData){
    return new Promise((resolve, reject)=> {
        if (!socket){
            reject("No socket connection")
            return
        }
        socket.emit(msgConstant, emitData, (data) => {
            // v pripade chyby socketio (napr timeout), vraci error string
            if (data.result){
                resolve(data.data)
            }else{
                // v pripade chyby socketio (napr timeout), nedostaneme zpatky objekt s {result, data}, ale error string - vratime error string
                reject(typeof data === "object" && "data" in data ? data.data : data)
            }
        })

        // timeout by mel nejlepe shodny s MAX_REQUEST_DURATION
        // TODO dodelat tak aby prevzalo z configu
        setTimeout(() => {
            reject("Server not responding (SocketIO timeout) during: " + msgConstant);
        }, 30000)
    })
}

export async function updateNode (socket, node, value){
    return actionCreator(socket, "UPDATE_NODE", {node, value})
}

export async function startCapture (socket, deviceInfo){
    return actionCreator(socket, "START_CAPTURE", deviceInfo)
}

export async function stopCapture (socket){
    return actionCreator(socket, "STOP_CAPTURE")
}

export async function getDevices (socket){
    return actionCreator(socket, "GET_DEVICES")
}

export async function getConfig (socket){
    return actionCreator(socket, "GET_CONFIG")
}

export async function getMeasData (socket){
    return actionCreator(socket, "GET_MEAS_DATA")
}