// ========================================
// Media Manager
// Responsible for camera and microphone
// ========================================

let localStream = null;

export async function startLocalCamera(videoElement) {

    try {

        localStream = await navigator.mediaDevices.getUserMedia({

            video: true,
            audio: false

        });

        videoElement.srcObject = localStream;

        console.log("✅ Local camera started");

        return localStream;

    }

    catch(error){

        console.error(error);

        throw error;

    }

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