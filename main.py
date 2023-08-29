from libprobe.probe import Probe
from lib.check.a import check_a
from lib.check.aaaa import check_aaaa
from lib.check.caa import check_caa
from lib.check.cname import check_cname
from lib.check.ds import check_ds
from lib.check.mx import check_mx
from lib.check.ns import check_ns
from lib.check.ptr import check_ptr
from lib.check.soa import check_soa
from lib.check.srv import check_srv
from lib.check.txt import check_txt
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'A': check_a,
        'AAAA': check_aaaa,
        'CAA': check_caa,
        'CNAME': check_cname,
        'DS': check_ds,
        'MX': check_mx,
        'NS': check_ns,
        'PTR': check_ptr,
        'SOA': check_soa,
        'SRV': check_srv,
        'TXT': check_txt,
    }

    probe = Probe("dns", version, checks)

    probe.start()
