console.log("📹 Recordings page loaded");

const recordingsList = document.getElementById("recordingsList");
const videoPlayer = document.getElementById("videoPlayer");

const totalVideos = document.getElementById("totalVideos");
const totalStorage = document.getElementById("totalStorage");

async function loadRecordings() {

    try {

        const response = await fetch("/videos/");
        const videos = await response.json();

        // ==========================
        // Dashboard Statistics
        // ==========================

        totalVideos.textContent = videos.length;

        const totalBytes = videos.reduce(
            (sum, video) => sum + (video.file_size || 0),
            0
        );

        totalStorage.textContent =
            `${(totalBytes / (1024 * 1024)).toFixed(2)} MB`;

        recordingsList.innerHTML = "";

        if (videos.length === 0) {

            recordingsList.innerHTML =
                "<p>No recordings found.</p>";

            return;
        }

        videos.forEach(video => {

            const card = document.createElement("div");

            card.className = "video-card";

            card.innerHTML = `

                <div class="video-header">

                    <h3>📹 Flight Recording</h3>

                </div>

                <div class="video-info">

                    <p>

                        <strong>Filename</strong><br>

                        ${video.filename}

                    </p>

                    <p>

                        <strong>Uploaded</strong><br>

                        ${new Date(video.uploaded_at).toLocaleString()}

                    </p>

                    <p>

                        <strong>File Size</strong><br>

                        ${(video.file_size / (1024 * 1024)).toFixed(2)} MB

                    </p>

                </div>

                <div class="video-actions">

                    <button
                        class="play-btn"
                        data-id="${video.id}">

                        ▶ Play

                    </button>

                    <button
                        class="download-btn"
                        data-id="${video.id}">

                        ⬇ Download

                    </button>

                    <button
                        class="delete-btn"
                        data-id="${video.id}">

                        🗑 Delete

                    </button>

                </div>

            `;

            recordingsList.appendChild(card);

            // ==========================
            // Play
            // ==========================

            const playButton =
                card.querySelector(".play-btn");

            playButton.addEventListener("click", () => {

                videoPlayer.src =
                    `/videos/${video.id}/stream`;

                videoPlayer.load();

                videoPlayer.play();

                videoPlayer.scrollIntoView({
                    behavior: "smooth"
                });

            });

            // ==========================
            // Download
            // ==========================

            const downloadButton =
                card.querySelector(".download-btn");

            downloadButton.addEventListener("click", () => {

                const link = document.createElement("a");

                link.href =
                    `/videos/${video.id}/stream`;

                link.download = video.filename;

                document.body.appendChild(link);

                link.click();

                document.body.removeChild(link);

            });

            // ==========================
            // Delete
            // ==========================

            const deleteButton =
                card.querySelector(".delete-btn");

            deleteButton.addEventListener("click", async () => {

                const confirmDelete = confirm(
                    "Delete this recording?"
                );

                if (!confirmDelete) {
                    return;
                }

                try {

                    const response = await fetch(
                        `/videos/${video.id}`,
                        {
                            method: "DELETE",
                        }
                    );

                    if (!response.ok) {

                        throw new Error(
                            "Failed to delete recording."
                        );

                    }

                    alert("Recording deleted successfully.");

                    // Refresh the recordings list
                    loadRecordings();

                }

                catch (error) {

                    console.error(error);

                    alert("Could not delete recording.");

                }

            });

        });

    }

    catch (error) {

        console.error(error);

    }

}

loadRecordings();