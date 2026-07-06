import {
    createPeerConnection,
    addIceCandidate,
    getPeerConnection,
    getRemoteStream
} from "./webrtc.js";

const statusText = document.getElementById("statusText");
const remoteVideo = document.getElementById("remoteVideo");
const startRecordingBtn = document.getElementById("startRecording");
const stopRecordingBtn = document.getElementById("stopRecording");

const wsProtocol =
    location.protocol === "https:" ? "wss" : "ws";

const socket = new WebSocket(
    `${wsProtocol}://${location.host}/ws/dashboard`
);
let remoteStream = null;  
let mediaRecorder = null;
let recordedChunks = [];  

socket.onopen = () => {

    console.log("✅ Dashboard Connected");

    statusText.textContent =
        "Connected to backend.";

};

// socket.onmessage = async (event) => {

//     const data = JSON.parse(event.data);

//     console.log("📨", data);

//     if (data.type === "offer") {

//     console.log("🎉 Offer received!");

//     const peerConnection =
//         createPeerConnection(remoteVideo);

//         await peerConnection.setRemoteDescription(
//             new RTCSessionDescription(data.sdp)
//     );
    
//     if (data.type === "candidate") {

//     console.log("🧊 Candidate received");

//     await addIceCandidate(data.candidate);

//     }

    
//     console.log("✅ Remote Description Set");
        
//     const answer = await peerConnection.createAnswer();

//     await peerConnection.setLocalDescription(answer);

//     console.log("✅ Answer Created");

//     socket.send(
//     JSON.stringify({

//         target: "phone_001",

//         type: "answer",

//         sender: "dashboard",

//         sdp: answer

//     })
//     );

//     console.log("📤 Answer Sent");

//     statusText.textContent = "Answer Sent";


//     statusText.textContent =
//         "Offer Received";

// }

// };
socket.onmessage = async (event) => {

    const data = JSON.parse(event.data);

    console.log("📨", data);

    if (data.type === "offer") {

        console.log("🎉 Offer received!");

        const peerConnection =
            createPeerConnection(remoteVideo);

        await peerConnection.setRemoteDescription(
            new RTCSessionDescription(data.sdp)
        );

        console.log("✅ Remote Description Set");

        const answer =
            await peerConnection.createAnswer();

        await peerConnection.setLocalDescription(answer);

        console.log("✅ Answer Created");

        socket.send(
            JSON.stringify({
                target: "phone_001",
                type: "answer",
                sender: "dashboard",
                sdp: answer
            })
        );

        console.log("📤 Answer Sent");
       

        setTimeout(() => {

            const stream = getRemoteStream();

            console.log("🎥 Remote Stream:", stream);

        }, 1000);

    }

    // <-- THIS IS A SEPARATE if

    if (data.type === "candidate") {

        console.log("🧊 Candidate received");

        await addIceCandidate(data.candidate);

    }

};

socket.onerror = () => {

    statusText.textContent =
        "Connection Error.";

};

socket.onclose = () => {

    statusText.textContent =
        "Disconnected.";

};
startRecordingBtn.onclick = () => {

    console.log("🎬 Start Recording button clicked");

    const stream = getRemoteStream();

    console.log("🎥 Stream:", stream);
    if (!stream) {

    alert("Remote stream not available yet!");

    return;

}

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.onstop = () => {

    console.log("✅ Recording Stopped");

            const recordedVideo = new Blob(recordedChunks, {
                type: "video/webm"
            });

            console.log("🎥 Recorded Video Blob:", recordedVideo);
            const formData = new FormData();

            formData.append(
            "video",
            recordedVideo,
            "recording.webm"
);

console.log("📤 Upload Ready");
        fetch("/videos/upload", {
        method: "POST",
        body: formData
})
.then(response => response.json())
.then(data => {

    console.log("✅ Upload Successful");

    console.log(data);

})
.catch(error => {

    console.error("❌ Upload Failed");

    console.error(error);

});
            const videoURL = URL.createObjectURL(recordedVideo);

        const downloadLink = document.createElement("a");

        downloadLink.href = videoURL;

        downloadLink.download = "recording.webm";

        downloadLink.click();

        URL.revokeObjectURL(videoURL);

};

    console.log("🎥 MediaRecorder:", mediaRecorder);
    mediaRecorder.start(1000);

    console.log("🔴 Recording Started");    
    startRecordingBtn.disabled = true;
    stopRecordingBtn.disabled = false;
    mediaRecorder.ondataavailable = (event) => {

    console.log("📦 Chunk received:", event.data);

    if (event.data.size > 0) {

        recordedChunks.push(event.data);

        console.log("📁 Total Chunks:", recordedChunks.length);

    }

};

};
stopRecordingBtn.onclick = () => {

    console.log("⏹️ Stop Recording button clicked");

    mediaRecorder.stop();

};
