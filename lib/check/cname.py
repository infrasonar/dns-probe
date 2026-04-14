from libprobe.asset import Asset
from libprobe.check import Check
from dns import rdatatype
from ..utils import dns_check


QTYPE = rdatatype.CNAME


class CheckCNAME(Check):
    key = QTYPE.name

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:
        res = await dns_check(asset, local_config, config, QTYPE, True)
        return res
