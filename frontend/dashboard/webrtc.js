// =====================================
// Dashboard WebRTC
// =====================================

let peerConnection = null;
let remoteStream = null;

export function createPeerConnection(remoteVideo) {

    peerConnection = new RTCPeerConnection({

        iceServers: [
            {
                urls: "stun:stun.l.google.com:19302"
            }
        ]

    });

  peerConnection.ontrack = (event) => {

    console.log("✅ Remote stream received");

    remoteStream = event.streams[0];

    remoteVideo.srcObject = remoteStream;

};

    return peerConnection;

}

export function getPeerConnection() {

    return peerConnection;

}
export async function addIceCandidate(candidate) {

    if (!peerConnection) {
        throw new Error("PeerConnection not created");
    }

    await peerConnection.addIceCandidate(
        new RTCIceCandidate(candidate)
    );

    console.log("🧊 ICE Candidate Added");

}
export function getRemoteStream() {

    return remoteStream;

}