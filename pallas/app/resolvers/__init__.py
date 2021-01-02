from ariadne import make_executable_schema, load_schema_from_path, QueryType
from ariadne import snake_case_fallback_resolvers, convert_kwargs_to_snake_case
import time

type_defs = load_schema_from_path('schema.graphql')

query = QueryType()

@convert_kwargs_to_snake_case
@query.field('nowPlaying')
def resolve_now_playing(_, info):
    request = info.context
    return {
        "__typename": "Video",
        "name": "Key and Peele",
        "uri": "http://192.168.1.22:8000/nick.mp4",
        "last_played_epoch": int(time.time())
    }

schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)
