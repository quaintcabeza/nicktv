from datetime import datetime
import logging
import os
from pymongo import MongoClient


logger = logging.getLogger('gunicorn.error.' + __name__)


class DbBridge:
    @staticmethod
    def get_instance():
        mongo_uri = f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017"
        client = MongoClient(mongo_uri)
        db = client[os.environ['MONGODB_DATABASE']]
        return DbBridge(db)

    def __init__(self, db):
        self.db = db

    def add_to_schedule(self, show_times):
        show_time_entries = [
            {
                "name": entry['name'],
                "start_time_epoch": self._datetime_str_to_epoch(entry['showStart']),
                "end_time_epoch": self._datetime_str_to_epoch(entry['showEnd']),
                "write_time_epoch": self._datetime_to_epoch(datetime.now())
            }
            for entry in show_times
        ]
        self.db.schedule.insert_many(show_time_entries)
        return True

    def get_latest_schedule(self, max_num_shows: int):
        entries = self.db.schedule.find().sort("start_time_epoch", -1).limit(max_num_shows)
        show_times = [
            {
                "name": show_time['name'],
                "showStart": self._datetime_epoch_to_str(show_time['start_time_epoch']),
                "showEnd": self._datetime_epoch_to_str(show_time['end_time_epoch'])
            }
            for show_time in entries
        ]
        return show_times

    def get_now_playing(self, now: datetime):
        now_epoch = self._datetime_to_epoch(now)

        now_playing = self.db.schedule.find_one(
            {
                "start_time_epoch": { "$lte": now_epoch },
                "end_time_epoch": { "$gte": now_epoch }
            }
        )
        if now_playing:
            return {
                "name": now_playing['name'],
                "showStart": self._datetime_epoch_to_str(now_playing['start_time_epoch']),
                "showEnd": self._datetime_epoch_to_str(now_playing['end_time_epoch'])
            }
        return None

    def mark_played(self, name: str, uri: str, played_time: datetime):
        entry = {
            "name": name,
            "uri": uri,
            "played_time_epoch": self._datetime_to_epoch(played_time),
            "write_time_epoch": self._datetime_to_epoch(datetime.now())
        }
        self.db.history.insert_one(entry)
        return True

    def get_last_played(self, name):
        episode_entry = self.db.history.find_one({
            "name": name
        }, sort=[("played_time_epoch", -1)])
        if episode_entry:
            return {
                "name": episode_entry['name'],
                "uri": episode_entry['uri'],
                "lastPlayed": self._datetime_epoch_to_str(episode_entry['played_time_epoch'])
            }
        return None

    @classmethod
    def _datetime_to_epoch(cls, datetime_obj):
        return int(datetime_obj.timestamp())

    @classmethod
    def _datetime_str_to_epoch(cls, datetime_str):
        return cls._datetime_to_epoch(datetime.fromisoformat(datetime_str))

    @classmethod
    def _datetime_epoch_to_str(cls, epoch):
        return datetime.fromtimestamp(epoch).isoformat()
