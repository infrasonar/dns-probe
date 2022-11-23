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
        'a': check_a,
        'aaaa': check_aaaa,
        'caa': check_caa,
        'cname': check_cname,
        'ds': check_ds,
        'mx': check_mx,
        'ns': check_ns,
        'ptr': check_ptr,
        'soa': check_soa,
        'srv': check_srv,
        'txt': check_txt
    }

    probe = Probe("dns", version, checks)

    probe.start()
