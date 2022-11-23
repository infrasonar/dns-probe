import logging
from libprobe.asset import Asset


async def check_dns(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    ...
