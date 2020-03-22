
from datetime import datetime
"""
Gets a list of timestamps and flattens them in a way, that a slot logic accompanied with its load is visible
"""

def flatten_reservations(reservation_timeslots):
    # Flatten to a single list of timestamp-strings
    flattened_timestamps = [item for sublist in reservation_timeslots for item in sublist]

    # 48 Slots per day (2 per hour)
    buckets = [0] * 48

    # Iterate all timestamps and put them into their respective buckets
    for timestamp in flattened_timestamps:
        parsed_time = None
        try:
            if type(timestamp) is not datetime:
                # Example of time format "2020-03-22T08:00:00+0000"
                parsed_time = datetime.strptime(str(timestamp), '%Y-%m-%dT%H:%M:%S%z')
            else:
                parsed_time = timestamp

            if parsed_time is None:
                raise ValueError

        except Exception as e:
            print('[ERROR] While parsing timestamp', timestamp)
            print('[ERROR]   ', e)
            print('[ERROR] Ignoring this timestamp')

            continue

        bucket_index = 2 * parsed_time.hour
        if parsed_time.minute >= 30:
            bucket_index += 1

        buckets[bucket_index] += 1

    return buckets
