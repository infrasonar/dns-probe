from libprobe.asset import Asset
from ..dns_query import dns_query
from ..utils import get_state, check_config_field


def on_item(itm: dict) -> dict:
    return {
        'name': itm['data'],
        'address': itm['data'],
        'ttl': int(itm['ttl']),
    }


async def check_ptr(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    check_config_field(check_config, 'ptr')
    ptr = check_config.get('ptr', None)
    name_servers = check_config.get('nameServers', None)
    rows, measurement_time = await dns_query(ptr, 'ptr', name_servers)
    return get_state('ptr', rows, measurement_time, on_item)
