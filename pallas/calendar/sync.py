#!/usr/local/bin/python3

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
import googleapiclient.discovery
from google.oauth2 import service_account
import logging
import pyrfc3339
import requests
import sys
import pytz

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Show:
    name: str
    start_time: datetime
    end_time: datetime


def get_shows_starting_within_time_slot(time_slot_start, time_slot_end):
    SERVICE_ACCOUNT_FILE = '/secrets/calendar-service-account-key.json'
    NICKTV_ID = 'naarr31b8kbhqqdf9sb8kikmpc@group.calendar.google.com'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes= ['https://www.googleapis.com/auth/calendar.readonly']
    )
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials, cache_discovery=False)

    events_result = service.events().list(
        calendarId=NICKTV_ID,
        singleEvents=True,
        timeMin=time_slot_start.isoformat(),  # Lower bound for event's end time, exclusive
        timeMax=time_slot_end.isoformat()     # Upper bound for event's start time, exclusive
    ).execute()
    events = events_result.get('items', [])

    shows = [
        Show(
            name=event['summary'],
            start_time=pyrfc3339.parse(event['start']['dateTime']),
            end_time=pyrfc3339.parse(event['end']['dateTime'])
        )
        for event in events if 'dateTime' in event['start']  # Ignore all-day events
    ]

    filtered_shows = [
        show for show in shows if show.start_time >= time_slot_start
    ]

    return filtered_shows


def add_shows_to_schedule(shows):
    show_times_str = ", ".join([
        f"{{ name: \"{show.name}\", showStart: \"{show.start_time.isoformat()}\", showEnd: \"{show.end_time.isoformat()}\" }}"
        for show in shows
    ])
    payload = {
        "query": f"mutation AddToSchedule {{ addToSchedule(showTimes: [{show_times_str}]) }}"
    }

    response = requests.post('http://webserver:80/graphql', json=payload)
    if ('errors' in response.json()):
        raise Exception(response.json()['errors'])


def main():
    logger.info(f"Starting calendar sync")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--time_slot_start',
        type=int,
        help='Start of time slot in which to look for shows, specified in minutes past current hour',
        required=True,
        choices=range(0, 90)
    )
    parser.add_argument(
        '--time_slot_end',
        type=int,
        help='End of time slot in which to look for shows, specified in minutes past current hour',
        required=True,
        choices=range(1, 91)
    )
    args = parser.parse_args()
    assert(args.time_slot_start < args.time_slot_end)

    now = datetime.utcnow()
    time_slot_start = datetime(now.year, now.month, now.day, now.hour, tzinfo=pytz.UTC) + timedelta(minutes=args.time_slot_start)
    time_slot_end = datetime(now.year, now.month, now.day, now.hour, tzinfo=pytz.UTC) + timedelta(minutes=args.time_slot_end)
    logger.info(f"Looking for scheduled shows in: ({time_slot_start}, {time_slot_end})")

    shows = get_shows_starting_within_time_slot(time_slot_start, time_slot_end)
    if (shows):
        logger.info(f"Scheduled shows found: {shows}")
        add_shows_to_schedule(shows)
    else:
        logger.info("No scheduled shows found")


if __name__ == "__main__":
  main()

