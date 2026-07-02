// ================================
// Camera Page JavaScript
// ================================
import {

    startLocalCamera,
    stopLocalCamera

} from "./media.js";

// Video preview element
const localVideo = document.getElementById("localVideo");

// Buttons
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

// Status text
const statusText = document.getElementById("statusText");

// Stores the active camera stream
let localStream = null;

//function needs change 
async function startCamera(){

    try{

        await startLocalCamera(localVideo);

        statusText.textContent =
            "Camera Started";

    }

    catch(error){

        statusText.textContent =
            "Camera Failed";

    }

}

console.log("Camera page loaded successfully.");

console.log(localVideo);
console.log(startBtn);
console.log(stopBtn);
console.log(statusText);

startBtn.addEventListener("click", () => {

    socket.send(
        JSON.stringify({

            target: "dashboard",

            type: "hello",

            sender: "phone_001",

            message: "Hello Dashboard!"

        })
    );

});

stopBtn.addEventListener("click", () => {

    stopLocalCamera();

    statusText.textContent =
        "Camera Stopped";

});

const socket = new WebSocket("ws://localhost:8000/ws/phone_001");

socket.onopen = () => {

    console.log("✅ Camera Connected");

    statusText.textContent = "Connected to backend.";

};

socket.onmessage = (event) => {

    console.log("📨", event.data);

};

socket.onerror = (error) => {

    console.log(error);

};

socket.onclose = () => {

    console.log("Disconnected");

};