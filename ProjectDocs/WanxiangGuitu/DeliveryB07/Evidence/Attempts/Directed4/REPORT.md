# Local unattended validation
Root: D:\WanxiangValidationRuns\B07Directed4\20261024-225046-f3ef6c8f

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| B07Probe.Run | controlled | PASS | 0 | False |  |
| B07Rules.Run | controlled | PASS | 0 | False |  |
| B07Rules.Resume | controlled | FAIL | 1 | False |  |
| B07Rules.PendingResume | controlled | NOT_RUN |  | False | Dependency failed: B07Rules.Resume |
| B07Rules.CommittedResume | controlled | NOT_RUN |  | False | Dependency failed: B07Rules.PendingResume |
| B07Combat.Run | controlled | FAIL | 1 | False |  |
| B07Economy.Run | controlled | FAIL | 1 | False |  |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
