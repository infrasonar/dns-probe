import asyncio
import copy
import dns.asyncresolver
import dns.message
from dns.resolver import NoAnswer
from libprobe.exceptions import IgnoreResultException


def make_rr(simple, rdata):
    csimple = copy.copy(simple)
    csimple["data"] = rdata.to_text()
    return csimple


def flatten_rrset(rrs):
    simple = {}
    if len(rrs) > 0:
        simple["ttl"] = rrs.ttl
        return [make_rr(simple, rdata) for rdata in rrs]
    return [simple]


def to_dict(message):
    simple = []
    for rrs in message.answer:
        simple.extend(flatten_rrset(rrs))
    return simple


async def dns_query(qname: str, query_type: str, name_servers: list):
    aresolver = dns.asyncresolver.Resolver()

    if name_servers is not None:
        aresolver.nameservers = name_servers

    start = asyncio.get_event_loop().time()
    try:
        a = await aresolver.resolve(qname, query_type)
    except NoAnswer:
        raise IgnoreResultException
    except Exception:
        raise

    measurement_time = asyncio.get_event_loop().time() - start
    response = to_dict(a.response)
    return (response, measurement_time)
