# genery-downloader

A download helper for videos on [genery.io](https://genery.io)

## Install

### Requirements
- [Python 3](https://python.org)
- A Userscript Manager (Recommended: [Violentmonkey](https://violentmonkey.github.io/get-it/))
- [yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/Installation) (Make sure to put it in PATH)
- Python dependencies can be installed with
```shell
pip install -r requirements.txt
```
- To install the userscript, go to the Violentmonkey dashboard, and click the `+` sign and select Install from URL, and input the following URL:
```
<url>
```

- Or, click [here](url) and install the script from the Violentmonkey prompt.

 
## Usage

- Everytime you wish to download videos from [genery.io](https://genery.io), you need to run the download server, with:
```shell
python genery-server.py
```

- You can also run `genery-server.py` at startup, with the help of cronjobs (on UNIX-like environments) or Task Scheduler (Windows). It consumes negligible resources.

- You can then go on [genery.io](https://genery.io), and click on your desired video. You will get a prompt asking if you wish to download `Movie Title - Description.mp4`, and you can accept or deny the request as per your wisw.

- The videos will be downloaded in a `videos` directory, which will be situated in the same directory as `genery-server.py`.


## How it works

- The userscript intercepts XHRs that the website makes, and if it is the request to the API that returns details regarding the video (Title, Caption, hls stream url, etc.), the details get intercepted.

- These details are sent to the Flask download server (`genery-server.py`) running on port `2319` through a POST request. The download server then passes the hls stream url to `yt-dlp` and downloads it to the folder.

## Acknowledgement

- `genery-server.py` is a modified version of [ytdlp-monkey](https://github.com/eyeincide/ytdlp-monkey)'s `server.py`.
