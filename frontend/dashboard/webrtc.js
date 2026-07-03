// =====================================
// Dashboard WebRTC
// =====================================

let peerConnection = null;

export function createPeerConnection(remoteVideo) {

    peerConnection = new RTCPeerConnection({

        iceServers: [
            {
                urls: "stun:stun.l.google.com:19302"
            }
        ]

    });

    peerConnection.ontrack = (event) => {

        console.log("📹 Remote track received");

        remoteVideo.srcObject = event.streams[0];

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