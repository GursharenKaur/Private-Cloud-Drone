console.log("🚀 Dashboard Loaded");

import {
    createPeerConnection,
    addIceCandidate,
    getRemoteStream
} from "./webrtc.js";

// ======================================================
// DOM Elements
// ======================================================

const statusText = document.getElementById("statusText");
const remoteVideo = document.getElementById("remoteVideo");

const startRecordingBtn = document.getElementById("startRecording");
const stopRecordingBtn = document.getElementById("stopRecording");

// ======================================================
// WebSocket Connection
// ======================================================

const wsProtocol =
    location.protocol === "https:" ? "wss" : "ws";

const socket = new WebSocket(
    `${wsProtocol}://${location.host}/ws/dashboard`
);

// ======================================================
// Recording Variables
// ======================================================

let mediaRecorder = null;
let recordedChunks = [];

// ======================================================
// WebSocket Events
// ======================================================

socket.onopen = () => {

    console.log("✅ Dashboard Connected");

    statusText.textContent =
        "Connected to backend.";

};

socket.onerror = () => {

    console.error("WebSocket Error");

    statusText.textContent =
        "Connection Error.";

};

socket.onclose = () => {

    console.log("WebSocket Closed");

    statusText.textContent =
        "Disconnected.";

};

// ======================================================
// WebRTC Signaling
// ======================================================

socket.onmessage = async (event) => {

    const data = JSON.parse(event.data);

    console.log("📨", data);

    if (data.type === "offer") {

        console.log("🎉 Offer received");

        const peerConnection =
            createPeerConnection(remoteVideo);

        await peerConnection.setRemoteDescription(
            new RTCSessionDescription(data.sdp)
        );

        console.log("✅ Remote Description Set");

        const answer =
            await peerConnection.createAnswer();

        await peerConnection.setLocalDescription(answer);

        socket.send(
            JSON.stringify({
                target: "phone_001",
                sender: "dashboard",
                type: "answer",
                sdp: answer
            })
        );

        console.log("📤 Answer Sent");

    }

    if (data.type === "candidate") {

        console.log("🧊 ICE Candidate");

        await addIceCandidate(
            data.candidate
        );

    }

};

// ======================================================
// Start Recording
// ======================================================

startRecordingBtn.onclick = () => {

    console.log("🎬 Start Recording");

    const stream =
        getRemoteStream();

    if (!stream) {

        alert("Remote stream not available.");

        return;

    }

    recordedChunks = [];

    mediaRecorder =
        new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {

        if (event.data.size > 0) {

            recordedChunks.push(event.data);

        }

    };

    mediaRecorder.onstop = async () => {

        console.log("⏹ Recording Finished");

        const recordedVideo =
            new Blob(recordedChunks, {
                type: "video/webm"
            });

        // ==========================
        // Upload
        // ==========================

        const formData =
            new FormData();

        formData.append(
            "video",
            recordedVideo,
            "recording.webm"
        );

        try {

            const response =
                await fetch("/videos/upload", {

                    method: "POST",

                    body: formData

                });

            const result =
                await response.json();

            console.log(result);

        }

        catch (error) {

            console.error(error);

        }

        // ==========================
        // Local Download
        // ==========================

        const url =
            URL.createObjectURL(recordedVideo);

        const a =
            document.createElement("a");

        a.href = url;

        a.download = "recording.webm";

        a.click();

        URL.revokeObjectURL(url);

    };

    mediaRecorder.start(1000);

    startRecordingBtn.disabled = true;

    stopRecordingBtn.disabled = false;

    console.log("🔴 Recording Started");

};

// ======================================================
// Stop Recording
// ======================================================

stopRecordingBtn.onclick = () => {

    if (mediaRecorder) {

        mediaRecorder.stop();

    }

    startRecordingBtn.disabled = false;

    stopRecordingBtn.disabled = true;

};