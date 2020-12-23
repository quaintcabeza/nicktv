from ariadne import make_executable_schema, load_schema_from_path, QueryType
from ariadne import snake_case_fallback_resolvers, convert_kwargs_to_snake_case

type_defs = load_schema_from_path('schema.graphql')

query = QueryType()

@convert_kwargs_to_snake_case
@query.field('nowPlaying')
def resolve_now_playing(_, info):
    print("resolved resolve_now_playing")
    request = info.context
    return {
        "name": "Key and Peele",
        "episode": 1,
        "season": 2
    }

schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)
