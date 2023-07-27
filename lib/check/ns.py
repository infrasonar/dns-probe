from libprobe.asset import Asset
from ..utils import dns_check


QTYPE = 'NS'


async def check_ns(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    res = await dns_check(asset, asset_config, check_config, QTYPE, False)
    return res