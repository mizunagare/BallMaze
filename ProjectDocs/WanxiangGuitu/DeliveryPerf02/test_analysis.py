import unittest
from analyze_perf02 import quant,stats
from make_tables import valid_pdh
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
 def test_pdh_invalid_zero_not_valid_memory(self):
  self.assertFalse(valid_pdh({'actualAdapter':True,'Status':3221228486,'CookedValue':0}));self.assertTrue(valid_pdh({'actualAdapter':True,'Status':0,'CookedValue':0}))
 def test_other_adapter_and_nonfinite_rejected(self):
  self.assertFalse(valid_pdh({'actualAdapter':False,'Status':0,'CookedValue':123}));self.assertFalse(valid_pdh({'actualAdapter':True,'Status':0,'CookedValue':float('inf')}))
if __name__=='__main__':unittest.main(verbosity=2)
