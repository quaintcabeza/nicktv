from ariadne import make_executable_schema, load_schema_from_path, QueryType, MutationType
from ariadne import snake_case_fallback_resolvers, convert_kwargs_to_snake_case
import logging
import time


logger = logging.getLogger('gunicorn.error.' + __name__)


type_defs = load_schema_from_path('schema.graphql')


query = QueryType()

@convert_kwargs_to_snake_case
@query.field('nowPlaying')
def resolve_now_playing(_, info):
    anything_on = "nothing"

    if (anything_on == "video"):
        return {
            "__typename": "Video",
            "uri": "Key and Peele/Season 1/Episode 1",
            "name": "Key and Peele",
            "url": "http://192.168.1.22:8000/nick.mp4",
            "last_played_epoch": int(time.time())
        }
    elif (anything_on == "audio"):
        return {
            "__typename": "Audio",
            "uri": "Piper Jones/The Wandering Stars/Gordon Duncan Tunes",
            "name": "Piper Jones",
            "url": "http://192.168.1.22:8000/piper.mp3",
            "last_played_epoch": int(time.time())
        }
    else:
        return {
            "__typename": "NothingPlaying",
            "try_again_in_min": 0.5
        }


mutation = MutationType()

@convert_kwargs_to_snake_case
@mutation.field('markPlayed')
def resolve_mark_played(_, info, uri):
    return True


schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)
