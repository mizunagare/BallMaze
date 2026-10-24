# Local unattended validation
Root: D:\WanxiangValidationRuns\B07Directed\20261024-223000-d79ed648

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| B07Probe.Run | controlled | PASS | 0 | False |  |
| B07Rules.Run | controlled | FAIL | 1 | False |  |
| B07Rules.Resume | controlled | NOT_RUN |  | False | Dependency failed: B07Rules.Run |
| B07Rules.PendingResume | controlled | FAIL | 1 | False |  |
| B07Rules.CommittedResume | controlled | FAIL | 1 | False |  |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
