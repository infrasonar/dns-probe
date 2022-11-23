from libprobe.asset import Asset
from ..dns_query import dns_query
from ..utils import get_state, check_config_field


def on_item(itm: dict) -> dict:
    return {
        'name': itm['data'],
        'address': itm['data'],
        'ttl': int(itm['ttl']),
    }


async def check_a(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    check_config_field(check_config, 'fqdn')
    fqdn = check_config.get('fqdn', None)
    name_servers = check_config.get('nameServers', None)
    rows, measurement_time = await dns_query(fqdn, 'a', name_servers)
    return get_state('a', rows, measurement_time, on_item)
