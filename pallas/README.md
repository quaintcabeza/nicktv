# nicktv Pallas

### How to run service
```
$ export MEDIA_ROOT_DIR=/path/to/media/folder
$ export CALENDAR_SERVICE_ACCOUNT_KEY=/path/to/service/account/key
$ sudo -E make up-prod
```
Navigate to http://127.0.0.1:2222/graphql. Send this query:
```
mutation DoneWithMedia {
  markPlayed(name: "kp0", uri: "bobloblaw")
}

mutation AddToSchedule {
  addToSchedule(showTimes: [{
    name: "kp0",
    showStart: "2021-02-20T15:00:00",
    showEnd: "2021-02-20T16:00:00"
  }, {
    name: "heyA",
    showStart: "2021-02-20T09:30:00",
    showEnd: "2021-02-20T10:00:00"
  }])
}

query GetScheduleForToday {
  latestSchedule {
    name,
    showStart,
    showEnd
  }
}

query GetNowPlaying {
  nowPlaying {
    __typename
    ... on Video {
      uri,
      name,
      url,
      lastPlayed
    }
    ... on Audio {
      uri,
      name,
      url,
      lastPlayed
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

### How to configure Google Calendar API
- Create a new project in GCP.
- Enable Google Calendar API on the new project.
- Create a new service account.
    - Enable GSuite domain-wide delegation on the service account.
    - Create and download key for account.
- Go to your Calendar settings. Add the service account id in the `Share with specific people` section.
- The calendar has to be manually added to the service account. Run the following in a `venv`:
    ```
    pip install google-auth google-auth-httplib2 google-api-python-client
    ```

    Then execute the following py code:
    ```
    from google.oauth2 import service_account
    import googleapiclient.discovery

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'path/to/key.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    calendar_id = CALENDAR_ID_FROM_CALENDAR_SETTINGS

    calendar_list_entry = {
        'id': calendar_id
    }
    resp = service.calendarList().insert(body=calendar_list_entry).execute()
    ```

### Resources
- [What is GraphQL?](https://graphql.org/learn/)
- [Ariadne](https://ariadnegraphql.org/docs/intro)
- [Flask+Ariadne App](https://www.twilio.com/blog/graphql-api-python-flask-ariadne)
- [Google API Python Client Auth](https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md)
- [Google Calendar API Python Quickstart](https://developers.google.com/calendar/quickstart/python)
- [Google Calendar API Reference](https://developers.google.com/calendar/v3/reference/events)
- https://blog.knoldus.com/running-a-cron-job-in-docker-container/
- https://www.marmanold.com/tech/cron-in-docker-with-debian-slim/
