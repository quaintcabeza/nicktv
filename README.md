# nicktv
TV simulation for Roku

Starting template here: https://github.com/rokudev/samples/tree/0b92a931ff5f5959e8d8f9361c9bfda012dbb143/media/VideoExample

### Roadmap
- [x] Hello World on Roku
- [x] Roku app retrieves statically video file from the Internet and displays it in "TV" mode
- [x] Roku app retrieves statically served video file from local server
- [ ] Roku app retrieves streamed video file from local server
- [ ] Roku app hits API to retrieve hardcoded URL/Metadata for Video/Audio/Text display
- [ ] API has hardcoded scheduled videos
- [ ] Roku app hits API after currently playing video ends
- [ ] API hits Calendar to retrieve scheduled videos
- [ ] API is "smart" about episodes for TV series

### Known Bugs
- [ ] Pressing left/right button on Roku will pause video
- [ ] Large videos will not play properly, the server will time out

### How to run
- Follow instructions [here](https://developer.roku.com/docs/developer-program/getting-started/hello-world.md) 
to get started on installing Roku apps on your device. Note, if your browser is not able to open the Roku package upload page, try using an incognito window.
- Start a static file server by running the following on the device containing the video you want to play
    ```
    python3 -m http.server
    ```
- Update the video URL in `videoscene.xml` to the right IP+path, and then run the following to generate a zip file that you can upload to your Roku device.
    ```
    ./build.sh
    ```
- Open your new app on Roku. Cheers.
