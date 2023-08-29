import asyncio
import unittest
from lib.check.a import check_a
from lib.check.cname import check_cname
from libprobe.exceptions import (
    IncompleteResultException,
    CheckException,
)


def _run(fqdn=None, name_servers=['8.8.8.8'], check=None):
    check_config = {
        'fqdn': fqdn,
        'nameServers': name_servers
    }
    result = asyncio.run(check(None, None, check_config))
    return result


class TestProbe(unittest.TestCase):

    def test_check_dns_cname(self):
        q = 'CNAME'
        res = _run('www.cesbit.com', check=check_cname)
        self.assertIn(q, res)
        self.assertEqual(len(res[q]), 1)
        self.assertEqual(res[q][0]['record'], 'cesbit.com.')
        self.assertIsInstance(res[q][0]['timeit'], float)

    def test_check_dns_multi(self):
        q = 'A'
        res = _run(
            'www.cesbit.com',
            name_servers=['8.8.4.4', '8.8.8.8'],
            check=check_a)
        self.assertEqual(len(res[q]), 2)
        self.assertEqual(res[q][0]['name'], '8.8.4.4')
        self.assertEqual(res[q][1]['name'], '8.8.8.8')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestProbe('test_check_dns_cname'))
    suite.addTest(TestProbe('test_check_dns_multi'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
