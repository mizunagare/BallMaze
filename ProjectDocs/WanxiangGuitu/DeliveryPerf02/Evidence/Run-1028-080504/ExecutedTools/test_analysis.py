import unittest
from analyze_perf02 import quant,stats
class Tests(unittest.TestCase):
 def test_missing_not_zero(self):
  self.assertEqual(stats([],100)['status'],'NOT_RUN');self.assertIsNone(stats([],100)['p95'])
 def test_partial_kept(self):
  s=stats([1,2],4);self.assertEqual(s['missing'],2);self.assertEqual(s['status'],'UNRESOLVED')
 def test_known_percentiles(self):
  self.assertEqual(quant(list(range(1,11)),.5),5.5);self.assertAlmostEqual(quant(list(range(1,11)),.95),9.55)
 def test_valid_zero_count(self):
  self.assertEqual(stats([0,0],2)['p95'],0);self.assertEqual(stats([0,0],2)['status'],'PASS')
 def test_outlier_not_deleted(self):
  s=stats([1]*99+[1000],100);self.assertEqual(s['maximum'],1000);self.assertEqual(s['n'],100)
if __name__=='__main__':unittest.main(verbosity=2)
