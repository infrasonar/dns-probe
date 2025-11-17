from libprobe.probe import Probe
from lib.check.a import CheckA
from lib.check.aaaa import CheckAAAA
from lib.check.caa import CheckCAA
from lib.check.cname import CheckCNAME
from lib.check.ds import CheckDS
from lib.check.mx import CheckMX
from lib.check.ns import CheckNS
from lib.check.ptr import CheckPTR
from lib.check.soa import CheckSOA
from lib.check.srv import CheckSRV
from lib.check.txt import CheckTXT
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckA,
        CheckAAAA,
        CheckCAA,
        CheckCNAME,
        CheckDS,
        CheckMX,
        CheckNS,
        CheckPTR,
        CheckSOA,
        CheckSRV,
        CheckTXT,
    )

    probe = Probe("dns", version, checks)

    probe.start()
