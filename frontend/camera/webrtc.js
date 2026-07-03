// ======================================
// WebRTC Manager
// ======================================

let peerConnection = null;

export function createPeerConnection() {

    peerConnection = new RTCPeerConnection({

        iceServers: [

            {
                urls: "stun:stun.l.google.com:19302"
            }

        ]

    });

    peerConnection.onicecandidate = (event) => {

    if (event.candidate) {

        console.log("🧊 ICE Candidate Generated");

        console.log(event.candidate);
        window.sendIceCandidate(event.candidate);
    } else {

        console.log("✅ ICE Gathering Finished");

    }

    };

    console.log("✅ Peer Connection Created");

    return peerConnection;

}

export async function createOffer() {

    if (!peerConnection) {
        throw new Error("PeerConnection not created");
    }

    const offer = await peerConnection.createOffer();

    await peerConnection.setLocalDescription(offer);

    console.log("✅ SDP Offer Created");

    console.log(offer);

    return offer;
}

export function addLocalTracks(stream) {

    stream.getTracks().forEach(track => {

        peerConnection.addTrack(track, stream);

        console.log("📹 Track Added:", track.kind);

    });

    console.log(
    "Number of Senders:",
    peerConnection.getSenders().length
    );

    console.log(peerConnection);

}

export function getPeerConnection(){

    return peerConnection;

}

export async function setRemoteAnswer(answer) {

    if (!peerConnection) {
        throw new Error("PeerConnection not created");
    }

    await peerConnection.setRemoteDescription(
        new RTCSessionDescription(answer)
    );

    console.log("✅ Remote Answer Set");

}