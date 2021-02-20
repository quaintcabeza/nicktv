from ariadne import make_executable_schema, load_schema_from_path, QueryType, MutationType
from datetime import datetime
from .db_bridge import DbBridge
import logging
import time


logger = logging.getLogger('gunicorn.error.' + __name__)


type_defs = load_schema_from_path('schema.graphql')
query = QueryType()
mutation = MutationType()

db_bridge = DbBridge.get_instance()


@mutation.field('addToSchedule')
def resolve_add_to_schedule(_, info, showTimes):
    return db_bridge.add_to_schedule(showTimes)

@query.field('latestSchedule')
def resolve_latest_schedule(_, info):
    return db_bridge.get_latest_schedule(10)

@query.field('nowPlaying')
def resolve_now_playing(_, info):
    now_playing = db_bridge.get_now_playing(datetime.now())
    if not now_playing:
        return {
            "__typename": "NothingPlaying",
            "tryAgainInMin": 0.5
        }

    last_played_episode = db_bridge.get_last_played(now_playing['name'])
    anything_on = "video"

    if (anything_on == "video"):
        return {
            "__typename": "Video",
            "uri": "Key and Peele/Season 1/Episode 1",
            "name": "Key and Peele",
            "url": "http://192.168.1.22:8000/nick.mp4",
            "lastPlayed": datetime.now().isoformat()
        }
    elif (anything_on == "audio"):
        return {
            "__typename": "Audio",
            "uri": "Piper Jones/The Wandering Stars/Gordon Duncan Tunes",
            "name": "Piper Jones",
            "url": "http://192.168.1.22:8000/piper.mp3",
            "lastPlayed": datetime.now().isoformat()
        }

@mutation.field('markPlayed')
def resolve_mark_played(_, info, name, uri):
    return db_bridge.mark_played(name, uri, datetime.now())

schema = make_executable_schema(type_defs, query, mutation)
