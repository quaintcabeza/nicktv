# nicktv Roku App

### How to run
- Follow instructions [here](https://developer.roku.com/docs/developer-program/getting-started/hello-world.md) 
to get started on installing Roku apps on your device.
- To upload changes to Roku device:
    ```
    export ROKU_PASSWORD=your_password
    ./upload.sh
    ```
- To [debug](https://developer.roku.com/docs/developer-program/debugging/debugging-channels.md)
    ```
    telnet 192.168.1.7 8085
    ```
- Open your new app on Roku. Cheers.

### Resources
- Starting template here: https://github.com/rokudev/samples/tree/0b92a931ff5f5959e8d8f9361c9bfda012dbb143/media/VideoExample
- Making HTTP requests: https://rokulikeahurricane.io/everything_about_http
- Roku requests library: https://github.com/rokucommunity/roku-requests
- Using Task Nodes to make async requests: https://github.com/rokudev/samples/tree/master/ux%20components/control/TaskExample
