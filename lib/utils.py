import logging
import time
from typing import Optional, Any
from libprobe.asset import Asset
import asyncio
from dns import rdatatype, asyncresolver, flags
from dns.rdtypes.ANY.RRSIG import RRSIG
from dns.resolver import NoAnswer
from libprobe.exceptions import (
    CheckException,
    IgnoreCheckException,
    IncompleteResultException,
)


async def _time_dns(loop: asyncio.AbstractEventLoop,
                    aresolver: asyncresolver.Resolver,
                    qname: str,
                    qtype: str,
                    item: dict[str, Any],
                    single: bool) -> Optional[dict]:
    start = loop.time()
    try:
        response = (await aresolver.resolve(qname, qtype)).response
    except NoAnswer:
        return None
    except Exception as e:
        msg = str(e) or type(e).__name__
        raise CheckException(msg)  # this might result in a incomplete result
    else:
        rrsig: RRSIG | None = None
        for rrset in response.answer:
            if rrset.rdtype == rdatatype.RRSIG:
                frecord = rrset[0]
                if isinstance(frecord, RRSIG):
                    rrsig = frecord
                    break

        if rrsig:
            now = time.time()
            item['rrsig_inception'] = rrsig.inception
            item['rrsig_expiration'] = rrsig.expiration
            item['rrsig_is_valid'] = rrsig.inception <= now <= rrsig.expiration

            item['dnssec_enabled'] = True
        else:
            item['dnssec_enabled'] = False

        if single:
            record = response.answer[0].to_rdataset()[0]
            item['record'] = str(record)
        else:
            records = response.answer[0].to_rdataset()
            item['records'] = sorted(map(str, records))

        item['timeit'] = loop.time() - start


async def _dns_query(qname: str, qtype: str, name_server: str, single: bool):
    aresolver = asyncresolver.Resolver()

    try:
        aresolver.nameservers = [name_server]
    except ValueError as e:
        raise CheckException(str(e))

    # RD = Recursion Desired (default)
    # CD = Checking Disabled (ignore check, receive even if not valid)
    # AD = Authenticated Data (include to see if valid according nameserver)
    #      We exclude AD, as we need to choose between CD and AD
    aresolver.set_flags(flags.RD | flags.CD)

    # DO = DNSSEC OK (required to receive RRSIG)
    aresolver.use_edns(0, ednsflags=flags.DO)

    loop = asyncio.get_running_loop()
    item = {
        'name': name_server,
        'query': qname,
    }
    await _time_dns(loop, aresolver, qname, qtype, item, single)
    return item


async def dns_check(
        asset: Asset,
        local_config: dict,
        config: dict,
        qtype: str,
        single: bool) -> dict:
    name_servers = config.get('nameServers')
    if not name_servers or not isinstance(name_servers, (tuple, list)):
        logging.warning(
            'Check did not run; '
            'nameServers is not provided, invalid or empty')
        raise IgnoreCheckException

    qname = config.get('fqdn')
    if not qname:
        qname = asset.name

    items = []
    result = {qtype: items}
    check_exc: Optional[CheckException] = None
    for name_server in name_servers:
        try:
            item = await _dns_query(qname, qtype, name_server, single)
        except CheckException as e:
            check_exc = e
        else:
            items.append(item)

    if check_exc is None:
        return result
    elif items:
        raise IncompleteResultException(str(check_exc), result)
    raise check_exc
