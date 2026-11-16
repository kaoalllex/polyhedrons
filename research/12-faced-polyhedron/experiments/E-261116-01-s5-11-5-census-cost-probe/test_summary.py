"""Prevent censored prices and incomplete runs from opening the expensive follow-ups."""
import unittest
from summary import verdict


class PriceTests(unittest.TestCase):
    def sample(self, timeouts=0, seconds=30):
        queue = dict(maps=[dict(index=i) for i in range(10)], populations={'test':3986})
        rows = [dict(map_index=i, pattern='test', status='TIMEOUT' if i<timeouts else 'UNSAT-SOLVER',
                     models=[dict(seconds=3600 if i<timeouts else seconds)],
                     price_seconds=3600 if i<timeouts else seconds) for i in range(10)]
        return queue, rows

    def test_uncensored_cheap_sample_opens_sweep_and_s0(self):
        r=verdict(*self.sample())
        self.assertEqual(r['verdict'],'OWNER-SWEEP')
        self.assertTrue(r['s0_price_probe_allowed'])

    def test_five_timeouts_block_sweep_and_s0(self):
        r=verdict(*self.sample(5))
        self.assertEqual(r['verdict'],'NO-SWEEP-SYMMETRIC-SLICE')
        self.assertTrue(r['median_censored'])
        self.assertFalse(r['s0_price_probe_allowed'])

    def test_censored_price_does_not_open_sweep(self):
        queue,rows=self.sample(1)
        rows[0]['models'][0]['seconds']=1200
        rows[0]['price_seconds']=1200
        r=verdict(queue,rows)
        self.assertEqual(r['verdict'],'LEAD-REVIEW')
        self.assertTrue(r['s0_price_probe_allowed'])

    def test_expensive_complete_sample_parks_sweep(self):
        r=verdict(*self.sample(seconds=1201))
        self.assertEqual(r['verdict'],'NO-SWEEP-SYMMETRIC-SLICE')
        self.assertFalse(r['s0_price_probe_allowed'])

    def test_missing_and_duplicate_records_cannot_finish(self):
        queue,rows=self.sample()
        self.assertEqual(verdict(queue,rows[:-1])['verdict'],'INCOMPLETE')
        with self.assertRaises(ValueError):
            verdict(queue,rows+[rows[0]])
        rows[0]['status']='UNKNOWN'
        with self.assertRaises(ValueError):
            verdict(queue,rows)

    def test_sat_with_incomplete_bridge_has_priority(self):
        queue,rows=self.sample(5)
        rows[-1].update(status='SAT',bridge_complete=False)
        r=verdict(queue,rows)
        self.assertEqual(r['verdict'],'SAT-REVIEW')
        self.assertEqual(r['incomplete_model_sets'],[9])


if __name__=='__main__':
    unittest.main()
