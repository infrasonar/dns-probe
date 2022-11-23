import logging
from libprobe.exceptions import IgnoreResultException
from typing import Callable, List


def check_config_field(check_config: dict, field: str):
    val = check_config.get(field)
    if not val:
        logging.warning(
            f'Check did not run; {field} is not provided or empty')
        raise IgnoreResultException


def get_state(
        type_name: str,
        rows: List[dict],
        measurement_time: float,
        on_item: Callable[[dict], dict]) -> dict:
    return {
        type_name: [on_item(itm) for itm in rows],
        'stat': [{
            'name': 'timeit',
            'measuredTime': measurement_time
        }]
    }
