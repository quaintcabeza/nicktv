# nicktv Server

### How to run
```
$ python3 -m venv .
$ source bin/activate
$ pip install -r requirements.txt
$ FLASK_APP=main.py FLASK_ENV=development flask run --port 5000
```
Navigate to http://127.0.0.1:5000/graphql. Send this query:
```
query GetNowPlaying {
  nowPlaying {
    name,
    episode
  }
}
```

### Resources
- [What is GraphQL?](https://graphql.org/learn/)
- [Ariadne](https://ariadnegraphql.org/docs/intro)
- [Flask+Ariadne App](https://www.twilio.com/blog/graphql-api-python-flask-ariadne)
