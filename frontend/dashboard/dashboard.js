import {
    createPeerConnection,
    addIceCandidate,
    getPeerConnection
} from "./webrtc.js";

const statusText = document.getElementById("statusText");
const remoteVideo = document.getElementById("remoteVideo");

const wsProtocol =
    location.protocol === "https:" ? "wss" : "ws";

const socket = new WebSocket(
    `${wsProtocol}://${location.host}/ws/dashboard`
);

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