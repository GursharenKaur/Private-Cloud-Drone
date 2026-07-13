// ================================
// Camera Page JavaScript
// ================================
import {

    startLocalCamera,
    stopLocalCamera

} from "./media.js";

import {

    createPeerConnection,
    addLocalTracks,
    createOffer,
    setRemoteAnswer
} from "./webrtc.js";

// Video preview element
const localVideo = document.getElementById("localVideo");

// Buttons
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

// Status text
const statusText = document.getElementById("statusText");

// Stores the active camera stream

//let localStream = null;

//function needs change 
async function startCamera() {
    console.log("Inside startCamera");
    try {

        const stream = await startLocalCamera(localVideo);

        createPeerConnection();

        addLocalTracks(stream);

        const offer = await createOffer();

        console.log(offer);

        statusText.textContent = "Offer Created";

        socket.send(
            JSON.stringify({
            target: "dashboard",
            type: "offer",
            sender: "phone_001",
            sdp: offer
        })
    );

        console.log("📤 Offer sent");

    }
    catch(error){

    console.error("START CAMERA ERROR:", error);

    alert(error.name + "\n\n" + error.message);

    statusText.textContent = error.name;

}
}

console.log("Camera page loaded successfully.");

console.log(localVideo);
console.log(startBtn);
console.log(stopBtn);
console.log(statusText);

// startBtn.addEventListener("click", async () => {
//      console.log("🚀 Start button clicked");
//     await startCamera();

//     socket.send(
//         JSON.stringify({

//             target: "dashboard",

//             type: "hello",

//             sender: "phone_001",

//             message: "Hello Dashboard!"

//         })
//     );

// });
startBtn.addEventListener("click", async () => {

    console.log("🚀 Start button clicked");

    try {

        await startCamera();

        console.log("✅ startCamera() completed");

    } catch (err) {

        console.error("❌ Error:", err);

    }

});

stopBtn.addEventListener("click", () => {

    stopLocalCamera();

    statusText.textContent =
        "Camera Stopped";

});

const wsProtocol =
    location.protocol === "https:" ? "wss" : "ws";

// TEMPORARY - Phase 5.3 testing only
const deviceToken =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMDRhMjM1Ni0wYjE5LTQwOWUtOWQ4NS01YmE5Y2E2MTYxN2IiLCJ0eXBlIjoiZGV2aWNlIiwiZXhwIjoxNzgzOTI2ODY3fQ.IHGjgSPpfFeSzT5XrJz9P2XKvzG9kkk44waK7DNsCkI";

const wsUrl =
    `${wsProtocol}://${location.host}/ws/phone_001?token=${deviceToken}`;

console.log("WS URL:", wsUrl);
console.log("Device Token:", deviceToken);
alert(wsUrl);
const socket = new WebSocket(wsUrl);

window.sendIceCandidate = (candidate) => {

    socket.send(
        JSON.stringify({
            target: "dashboard",
            type: "candidate",
            sender: "phone_001",
            candidate: candidate
        })
    );

    console.log("📤 ICE Candidate Sent");

};

socket.onopen = () => {

    console.log("✅ Camera Connected");

    statusText.textContent = "Connected to backend.";

};

socket.onmessage = async (event) => {

    const data = JSON.parse(event.data);

    console.log("📨", data);

    if (data.type === "answer") {

        console.log("🎉 Answer received!");

        await setRemoteAnswer(data.sdp);

        console.log("✅ Phone negotiation completed");

        statusText.textContent =
            "Connected to Dashboard";

    }

};

socket.onerror = (error) => {

    console.log(error);

};

socket.onclose = () => {

    console.log("Disconnected");

};
console.log("Start Button Object:", startBtn);