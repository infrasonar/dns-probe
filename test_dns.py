import asyncio
import unittest
from lib.check.dns import check_dns
from libprobe.exceptions import (
    IncompleteResultException,
    CheckException,
)


def _run(fqdn=None, name_servers=['8.8.8.8']):
    check_config = {
        'fqdn': fqdn,
        'nameServers': name_servers
    }
    result = asyncio.run(check_dns(None, None, check_config))
    return result['dns']


class TestProbe(unittest.TestCase):

    def test_check_dns_cname(self):
        res = _run('www.cesbit.com')
        self.assertIn('CNAME', res[0])
        self.assertNotIn('A', res[0])
        self.assertEqual(1, res[0]['answers'])
        self.assertEqual(res[0]['query'], 'www.cesbit.com')
        self.assertIsInstance(res[0]['timeit'], float)
        self.assertIsInstance(res[0]['answers'], int)

    def test_check_dns_ptr(self):
        res = _run('4.4.8.8.in-addr.arpa')
        self.assertIn('PTR', res[0])
        self.assertNotIn('A', res[0])
        self.assertEqual(1, res[0]['answers'])

    def test_check_dns_more(self):
        res = _run('cesbit.com')
        self.assertNotIn('PTR', res[0])
        self.assertIn('A', res[0])
        self.assertGreater(res[0]['answers'], 5)

    def test_check_dns_incomplete(self):
        try:
            _run('www.cesbit.com', name_servers=['0.0', '8.8.8.8'])
        except IncompleteResultException as e:
            result = e.result
            self.assertIn('CNAME', result['dns'][0])
        else:
            raise Exception('IncompleteResultException not raised')

    def test_check_dns_multi(self):
        res = _run('www.cesbit.com', name_servers=['8.8.4.4', '8.8.8.8'])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['name'], '8.8.4.4')
        self.assertEqual(res[1]['name'], '8.8.8.8')
        self.assertEqual(1, res[0]['answers'])
        self.assertEqual(1, res[1]['answers'])

    def test_check_dns_incomplete(self):
        try:
            _run('www.cesbit.com', name_servers=['0.0', '8.8.8.8'])
        except IncompleteResultException as e:
            result = e.result
            self.assertIn('CNAME', result['dns'][0])
            self.assertRegex(str(e), r'nameserver 0.0 is not an IP address')
        else:
            raise Exception('IncompleteResultException not raised')

    def test_check_dns_check_exc(self):
        with self.assertRaisesRegex(
                CheckException,
                r'The resolution lifetime expired after'):
            _run('www.cesbit.com', name_servers=['8.8.8.0'])


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestProbe('test_check_dns_cname'))
    suite.addTest(TestProbe('test_check_dns_ptr'))
    suite.addTest(TestProbe('test_check_dns_more'))
    suite.addTest(TestProbe('test_check_dns_incomplete'))
    suite.addTest(TestProbe('test_check_dns_multi'))
    suite.addTest(TestProbe('test_check_dns_check_exc'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
