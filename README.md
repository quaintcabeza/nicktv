# nicktv

![Nick TV!](/roku/images/app_icon_fhd.jpg)

Old fashioned TV on Roku. Yay scheduled shows! Boo binge watching!

### Roadmap
- [x] Hello World on Roku
- [x] Roku app retrieves statically served video file from the Internet and displays it in "TV" mode
- [x] Roku app retrieves statically served video file from local server
- [ ] Roku app hits API to retrieve hardcoded URL+Metadata for Video/Audio/Text display
- [ ] API has hardcoded scheduled videos
- [ ] Roku app hits API after currently playing video ends
- [ ] API hits Calendar to retrieve scheduled videos
- [ ] API is "smart" about episodes for TV series

### Known Bugs
- [ ] Pressing left/right button on Roku will pause video

### How to run
- Follow instructions [here](https://developer.roku.com/docs/developer-program/getting-started/hello-world.md) 
to get started on installing Roku apps on your device. Note, if your browser is not able to open the Roku package upload page, try using an incognito window.
- Use an apache server to serve an `mp4` file (Note: Roku's `Video Node` does not support `avi` and `wmv`).
    - how to install apache: `sudo apt-get install apache2`
    - how to configure server ports: edit `/etc/apache2/ports.conf`
    - how to restart service: `sudo service apache2 restart`
    - how to serve files: remove `index.html` from `/var/www/html` and put your file (or symlink) here
- Update the video URL in `videoscene.xml` to the right IP+path, and then run the following to generate a zip file that you can upload to your Roku device.
    ```
    ./build.sh
    ```
- Open your new app on Roku. Cheers.

### Resources
Starting template here: https://github.com/rokudev/samples/tree/0b92a931ff5f5959e8d8f9361c9bfda012dbb143/media/VideoExample

