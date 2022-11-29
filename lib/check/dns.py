import logging
from typing import Optional
from libprobe.asset import Asset
import asyncio
import copy
import dns.asyncresolver
import dns.message
from dns.resolver import NoAnswer
from libprobe.exceptions import (
    CheckException,
    IgnoreCheckException,
    IncompleteResultException,
)


def get_item(timeit: float, answers: int, item: dict) -> dict:
    item['answers'] = answers
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
        return get_item(loop.time() - start, 1, item)


async def dns_multi(aresolver, qname, qtype, item) -> int:
    try:
        response = (await aresolver.resolve(qname, qtype)).response
    except NoAnswer:
        return 0
    except Exception as e:
        msg = str(e) or type(e).__name__
        raise CheckException(msg)  # this might result in a incomplete result
    else:
        records = response.answer[0].to_rdataset()
        item[qtype] = sorted(map(str, records))
        return 1


async def dns_query(qname: str, name_server: str):
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

    if (await dns_single(loop, aresolver, qname, 'CNAME', item)):
        return item
    if (await dns_single(loop, aresolver, qname, 'PTR', item)):
        return item

    answers = 0
    start = loop.time()
    answers += (await dns_multi(aresolver, qname, 'A', item))
    answers += (await dns_multi(aresolver, qname, 'AAAA', item))
    answers += (await dns_multi(aresolver, qname, 'CAA', item))
    answers += (await dns_multi(aresolver, qname, 'DS', item))
    answers += (await dns_multi(aresolver, qname, 'MX', item))
    answers += (await dns_multi(aresolver, qname, 'NS', item))
    answers += (await dns_multi(aresolver, qname, 'SOA', item))
    answers += (await dns_multi(aresolver, qname, 'SRV', item))
    answers += (await dns_multi(aresolver, qname, 'TXT', item))
    return get_item(loop.time() - start, answers, item)


async def check_dns(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    name_servers = check_config.get('nameServers')
    if not name_servers or not isinstance(name_servers, (tuple, list)):
        logging.warning(
            'Check did not run; '
            'nameServers is not provided, invalid or empty')
        raise IgnoreCheckException

    query = check_config.get('fqdn')
    if not query:
        query = asset.name

    items = []
    result = {'dns': items}
    check_exc: Optional[CheckException] = None
    for name_server in name_servers:
        try:
            item = await dns_query(query, name_server)
        except CheckException as e:
            check_exc = e
        else:
            items.append(item)

    if check_exc is None:
        return result
    elif items:
        raise IncompleteResultException(str(check_exc), result)
    raise check_exc
