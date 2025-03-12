from flask import Flask, request, jsonify
import os
import subprocess
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Default download directory relative to the script's location
# You can change this to an absolute path if needed, e.g., "/var/videos"
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")

@app.route("/youtube-dl", methods=["POST"])
def download_video():
    """
    Endpoint to trigger a yt-dlp download.

    Expected JSON payload:
    {
      "url": "<URL to the video>",
      "title": "title of video"
    }

    Example:
    {
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
      "title": "rickroll"
    }
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    video_url = data.get("url")
    if not video_url:
        return jsonify({"error": "Missing 'url' in request"}), 400

    video_title = data.get("title")
    if not video_url:
        return jsonify({"error": "Missing 'title' in request"}), 400
    # Ensure the download directory exists
    os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

    # Construct the yt-dlp command
    # Adjust quality and options as needed:
    # - "--cookies-from-browser firefox" removed, as it requires browser-specific setup.
    # - You can add or remove format selectors as needed.
    # - Ensure "yt-dlp" is in PATH or replace with a full path (e.g. "/usr/local/bin/yt-dlp").

    if os.path.exists(f"{DEFAULT_DOWNLOAD_DIR}/{video_title}.mp4"):
        app.logger.info(f"file {video_title}.mp4 exists")
        return jsonify({
            "message": "file exists"
            }), 200


    command = [
        "yt-dlp",
        "-o", f"{DEFAULT_DOWNLOAD_DIR}/{video_title}.%(ext)s",
        video_url
    ]

    app.logger.info("Starting download for URL: %s", video_url)
    try:
        # Run yt-dlp command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            app.logger.error("yt-dlp failed with error: %s", result.stderr)
            return jsonify({
                "error": "yt-dlp execution failed",
                "details": result.stderr.strip()
            }), 500

        app.logger.info("Download started successfully.")
        return jsonify({"message": "Download started successfully."}), 200

    except FileNotFoundError:
        # This occurs if yt-dlp is not found in PATH
        app.logger.error("yt-dlp not found. Ensure it is installed and in the system PATH.")
        return jsonify({"error": "yt-dlp not found in PATH"}), 500
    except Exception as e:
        # Handle unexpected exceptions
        app.logger.exception("An unexpected error occurred.")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=2319, debug=True)
