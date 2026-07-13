// ========================================
// Media Manager
// Responsible for camera and microphone
// ========================================

let localStream = null;

export async function startLocalCamera(videoElement) {

    console.log("STEP 1");

    console.log("navigator =", navigator);

    console.log("mediaDevices =", navigator.mediaDevices);

    const devices =
        await navigator.mediaDevices.enumerateDevices();

    console.log(devices);

    localStream =
        await navigator.mediaDevices.getUserMedia({

            video: true,
            audio: false

        });

    console.log("STEP 2");

    videoElement.srcObject = localStream;

    console.log("STEP 3");

    return localStream;
}

export function stopLocalCamera(){

    if(!localStream){

        return;

    }

    localStream.getTracks().forEach(track => {

        track.stop();

    });

    localStream = null;

    console.log("Camera stopped.");

}

export function getLocalStream(){

    return localStream;

}