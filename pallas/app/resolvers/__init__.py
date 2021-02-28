from datetime import datetime
import logging
import time
from ariadne import make_executable_schema, load_schema_from_path, QueryType, MutationType
from .db_bridge import DbBridge
from .media_bridge import MediaBridge


logger = logging.getLogger('gunicorn.error.' + __name__)


type_defs = load_schema_from_path('schema.graphql')
query = QueryType()
mutation = MutationType()

db_bridge = DbBridge.get_instance()
media_bridge = MediaBridge.get_instance()


@mutation.field('addToSchedule')
def resolve_add_to_schedule(_, info, showTimes):
    return db_bridge.add_to_schedule(showTimes)

@query.field('latestSchedule')
def resolve_latest_schedule(_, info):
    return db_bridge.get_latest_schedule(10)

@query.field('nowPlaying')
def resolve_now_playing(_, info):
    now_playing = db_bridge.get_now_playing(datetime.now())
    try_again_time = 1
    if not now_playing:
        logger.info("Did not find any scheduled shows")
        return {
            "__typename": "NothingPlaying",
            "tryAgainInMin": try_again_time
        }

    show_name = now_playing['name']
    logger.info(f"Scheduled show found: {now_playing}")

    last_played = db_bridge.get_last_played(show_name)
    # Check if show has already been played
    if last_played:
        last_played_time = datetime.fromisoformat(last_played['lastPlayed'])
        show_start_time = datetime.fromisoformat(now_playing['showStart'])
        if last_played_time > show_start_time:
            logger.info(f"Scheduled show {show_name} has been played already at {last_played_time}")
            return {
                "__typename": "NothingPlaying",
                "tryAgainInMin": try_again_time
            }

    last_played_uri = last_played['uri'] if last_played else None
    next_video_uri = media_bridge.get_next_video_uri(show_name, last_played_uri)
    if next_video_uri:
        return {
            "__typename": "Video",
            "uri": next_video_uri,
            "name": show_name,
            "url": "http://192.168.1.22:2222" + next_video_uri,
            "lastPlayed": last_played['lastPlayed'] if last_played else None
        }

    next_audio_uri = media_bridge.get_next_audio_uri(show_name, last_played_uri)
    if next_audio_uri:
        return {
            "__typename": "Audio",
            "uri": next_audio_uri,
            "name": show_name,
            "url": "http://192.168.1.22:2222" + next_audio_uri,
            "lastPlayed": last_played['lastPlayed'] if last_played else None
        }

    logger.info(f"No supported media found for: {show_name}")
    return {
        "__typename": "NothingPlaying",
        "tryAgainInMin": try_again_time
    }


@mutation.field('markPlayed')
def resolve_mark_played(_, info, name, uri):
    return db_bridge.mark_played(name, uri, datetime.now())

schema = make_executable_schema(type_defs, query, mutation)
