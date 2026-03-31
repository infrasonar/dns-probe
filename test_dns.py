import asyncio
import unittest
from lib.check.a import CheckA
from lib.check.cname import CheckCNAME
from libprobe.asset import Asset
from libprobe.check import Check


def _run(check: type[Check], fqdn: str, name_servers: list[str] = ['8.8.8.8']):
    asset = Asset(0, '', '')
    local_config = {}
    config = {
        'fqdn': fqdn,
        'nameServers': name_servers
    }
    result = asyncio.run(check.run(asset, local_config, config))
    return result


class TestProbe(unittest.TestCase):

    def test_check_dns_cname(self):
        q = 'CNAME'
        res = _run(CheckCNAME, 'www.cesbit.com')
        self.assertIn(q, res)
        self.assertEqual(len(res[q]), 1)
        self.assertEqual(res[q][0]['record'], 'ext-cust.squarespace.com.')
        self.assertIsInstance(res[q][0]['timeit'], float)

    def test_check_dns_multi(self):
        q = 'A'
        res = _run(
            CheckA,
            'www.cesbit.com',
            name_servers=['8.8.4.4', '8.8.8.8'])
        self.assertEqual(len(res[q]), 2)
        self.assertEqual(res[q][0]['name'], '8.8.4.4')
        self.assertEqual(res[q][1]['name'], '8.8.8.8')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestProbe('test_check_dns_cname'))
    suite.addTest(TestProbe('test_check_dns_multi'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
