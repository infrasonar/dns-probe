from libprobe.asset import Asset
from ..dns_query import dns_query
from ..utils import get_state, check_config_field


def on_item(itm: dict) -> dict:
    primary_ns, responsible_name, serial, refresh, retry, expire, minimum \
        = itm['data'].split(' ')
    return {
        'name': primary_ns,
        'primaryNS': primary_ns,
        'responsibleName': responsible_name,
        'serial': serial,
        'refresh': refresh,
        'retry': retry,
        'expire': expire,
        'minimum': minimum,
        'ttl': int(itm['ttl']),
    }


async def check_soa(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    check_config_field(check_config, 'fqdn')
    fqdn = check_config.get('fqdn', None)
    name_servers = check_config.get('nameServers', None)
    rows, measurement_time = await dns_query(fqdn, 'soa', name_servers)
    return get_state('soa', rows, measurement_time, on_item)
