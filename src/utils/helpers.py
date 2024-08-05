import json
import hashlib
from model.logging import logger
import pendulum
from proto.datetime_helpers import DatetimeWithNanoseconds
from pendulum.exceptions import ParserError


def load_json_file(file_path) -> list[dict] | list[None]:
    try:
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logger.info(f"Error: The file '{file_path}' does not exist.")
        return []
    except json.JSONDecodeError as e:
        logger.info(f"Error decoding JSON from the file '{file_path}': {e}")
        return []


def hash_datastore_key(key: str) -> str:
    key = key.replace(" ", "")
    return f"{hashlib.md5(key.encode('utf-8')).hexdigest()}_{key}"


def is_stored_older_than_inbound_timestamp(stored_timestamp: str, inbound_timestamp: str) -> bool:
    try:
        inbound_timestamp = pendulum.parse(inbound_timestamp)
        if isinstance(stored_timestamp, DatetimeWithNanoseconds):
            stored_timestamp = pendulum.datetime(stored_timestamp.year, stored_timestamp.month,
                                                 stored_timestamp.day,
                                                 stored_timestamp.hour, stored_timestamp.minute,
                                                 stored_timestamp.second,
                                                 stored_timestamp.microsecond)
        elif isinstance(stored_timestamp, str):
            stored_timestamp = pendulum.parse(stored_timestamp)

        else:
            raise Exception("Something went wrong with parsing the timestamps. Raising Error")

        return stored_timestamp < inbound_timestamp
    except ParserError as pe:
        raise Exception(f"Something went wrong with parsing the timestamps: {pe}. Raising Error")
