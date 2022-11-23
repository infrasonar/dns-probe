from libprobe.asset import Asset
from ..dns_query import dns_query
from ..utils import get_state, check_config_field


def on_item(itm: dict) -> dict:
    priority, weight, port, target = itm['data'].split(' ')
    return {
        'name': target,
        'port': int(port),
        'priority': int(priority),
        'target': target,
        'ttl': int(itm['ttl']),
        'weight': int(weight),
    }


async def check_srv(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    check_config_field(check_config, 'fqdn')
    fqdn = check_config.get('fqdn', None)
    name_servers = check_config.get('nameServers', None)
    rows, measurement_time = await dns_query(fqdn, 'srv', name_servers)
    return get_state('srv', rows, measurement_time, on_item)
