import logging
from typing import Optional
from libprobe.asset import Asset
import asyncio
import dns.asyncresolver
import dns.message
from dns.resolver import NoAnswer
from libprobe.exceptions import (
    CheckException,
    IgnoreCheckException,
    IncompleteResultException,
)


def get_item(timeit: float, answers: int, item: dict) -> dict:
    item['timeit'] = timeit
    return item


async def dns_single(loop, aresolver, qname, qtype, item) -> Optional[dict]:
    start = loop.time()
    try:
        response = (await aresolver.resolve(qname, qtype)).response
    except NoAnswer:
        return None
    except Exception as e:
        msg = str(e) or type(e).__name__
        raise CheckException(msg)  # this might result in a incomplete result
    else:
        record = response.answer[0].to_rdataset()[0]
        item[qtype] = str(record)
        item['timeit'] = loop.time() - start


async def dns_query(qname: str, qtype: str, name_server: str):
    aresolver = dns.asyncresolver.Resolver()
    try:
        aresolver.nameservers = [name_server]
    except ValueError as e:
        raise CheckException(str(e))

    loop = asyncio.get_event_loop()
    item = {
        'name': name_server,
        'query': qname,
    }
    await dns_single(loop, aresolver, qname, qtype, item)
    return item


async def dns_check(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        qtype: str) -> dict:
    name_servers = check_config.get('nameServers')
    if not name_servers or not isinstance(name_servers, (tuple, list)):
        logging.warning(
            'Check did not run; '
            'nameServers is not provided, invalid or empty')
        raise IgnoreCheckException

    qname = check_config.get('fqdn')
    if not qname:
        qname = asset.name

    type_name = qtype.lower()

    items = []
    result = {type_name: items}
    check_exc: Optional[CheckException] = None
    for name_server in name_servers:
        try:
            item = await dns_query(qname, qtype, name_server)
        except CheckException as e:
            check_exc = e
        else:
            items.append(item)

    if check_exc is None:
        return result
    elif items:
        raise IncompleteResultException(str(check_exc), result)
    raise check_exc
