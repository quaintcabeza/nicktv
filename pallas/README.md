# nicktv Pallas

### How to run service
```
$ make up
```
Navigate to http://127.0.0.1:2222/graphql. Send this query:
```
query GetNowPlaying {
  nowPlaying {
    __typename
    ... on Video {
      name,
      uri,
      lastPlayedEpoch
    }
    ... on NothingPlaying {
      tryAgainInMin
    }
  }
}
```

### How to run a file server
- Use an apache server to serve an `mp4` file (Note: Roku's `Video Node` does not support `avi` and `wmv`).
    - how to install apache: `sudo apt-get install apache2`
    - how to configure server ports: edit `/etc/apache2/ports.conf`
    - how to restart service: `sudo service apache2 restart`
    - how to serve files: remove `index.html` from `/var/www/html` and put your file (or symlink) here

### Resources
- [What is GraphQL?](https://graphql.org/learn/)
- [Ariadne](https://ariadnegraphql.org/docs/intro)
- [Flask+Ariadne App](https://www.twilio.com/blog/graphql-api-python-flask-ariadne)
