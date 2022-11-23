import asyncio
import unittest
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
from libprobe.exceptions import IgnoreResultException


def _setup(check, fqdn=None, ptr=None, name_servers=['8.8.8.8']):
    check_config = {
        'fqdn': fqdn,
        'ptr': ptr,
        'nameServers': name_servers
    }
    asyncio.run(check(None, None, check_config))


class TestProbe(unittest.TestCase):

    def test_check_a(self):
        _setup(check_a, 'siridb.com')

    def test_check_aaaa(self):
        _setup(check_aaaa, 'siridb.com')

    def test_check_caa(self):
        _setup(check_caa, 'docs.thingsdb.net')

    def test_check_cname(self):
        _setup(check_cname, 'docs.thingsdb.net')

    def test_check_ds(self):
        _setup(check_ds, 'siridb.com')

    def test_check_mx(self):
        _setup(check_mx, 'siridb.com')

    def test_check_ns(self):
        _setup(check_ns, 'siridb.com')

    def test_check_ptr(self):
        _setup(check_ptr, ptr='4.4.8.8.in-addr.arpa.')

    def test_check_soa(self):
        _setup(check_soa, 'cesbit.com')

    def test_check_srv(self):
        # TODO
        _setup(check_srv, '_sip._tls.o365.test-technology.nl')

    def test_check_txt(self):
        _setup(check_txt, 'siridb.com')

    def test_check_caa_no_answer(self):
        with self.assertRaises(IgnoreResultException):
            _setup(check_caa, 'cesbit.com')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestProbe('test_check_a'))
    suite.addTest(TestProbe('test_check_aaaa'))
    suite.addTest(TestProbe('test_check_caa'))
    suite.addTest(TestProbe('test_check_cname'))
    suite.addTest(TestProbe('test_check_ds'))
    suite.addTest(TestProbe('test_check_mx'))
    suite.addTest(TestProbe('test_check_ns'))
    suite.addTest(TestProbe('test_check_ptr'))
    suite.addTest(TestProbe('test_check_soa'))
    suite.addTest(TestProbe('test_check_srv'))
    suite.addTest(TestProbe('test_check_txt'))
    suite.addTest(TestProbe('test_check_caa_no_answer'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
