"""Known-value tests for the independent analysis layer, not Player business evidence."""
import unittest
from summarize_perf import quant,stats,valid_system_value

class AnalysisTests(unittest.TestCase):
 def test_known_linear_quantiles(self):
  values=[1,2,3,4,5,6,7,8,9,10]
  self.assertEqual(quant(values,.5),5.5);self.assertAlmostEqual(quant(values,.95),9.55);self.assertAlmostEqual(quant(values,.99),9.91)
 def test_empty_is_missing(self):
  s=stats([],5);self.assertEqual(s['status'],'NOT_RUN');self.assertIsNone(s['p50']);self.assertEqual(s['missing'],5)
 def test_partial_is_not_full_pass(self):
  s=stats([1,2],4);self.assertEqual(s['status'],'UNRESOLVED');self.assertEqual(s['missing'],2)
 def test_real_zero_is_valid_count(self):
  s=stats([0,0,0],3);self.assertEqual(s['status'],'PASS');self.assertEqual(s['p99'],0)
 def test_single(self):
  self.assertEqual(quant([17],.99),17)
 def test_sort_does_not_mutate_input(self):
  v=[9,1,4];quant(v,.95);self.assertEqual(v,[9,1,4])
 def test_outlier_is_not_removed(self):
  s=stats([1]*99+[1000],100);self.assertEqual(s['maximum'],1000);self.assertEqual(s['n'],100);self.assertAlmostEqual(s['p99'],10.99)
 def test_zero_system_counters_are_distinct_from_unavailable(self):
  self.assertTrue(valid_system_value('gpu_shared_bytes',0));self.assertTrue(valid_system_value('cpu_machine_pct',0));self.assertFalse(valid_system_value('working_set_bytes',0));self.assertFalse(valid_system_value('gpu_shared_bytes',-1))
if __name__=='__main__':unittest.main(verbosity=2)
