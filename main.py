from libprobe.probe import Probe
from lib.check.dns import check_dns
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {'dns': check_dns}

    probe = Probe("dns", version, checks)

    probe.start()
