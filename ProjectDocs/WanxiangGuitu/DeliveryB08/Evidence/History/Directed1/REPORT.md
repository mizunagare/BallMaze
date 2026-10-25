# Local unattended validation
Root: D:\WanxiangValidationRuns\B08Directed1\20261025-171540-7fcac9c7

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| B08Probe.Run | controlled | PASS | 0 | False |  |
| B08Rules.Run | controlled | FAIL | 1 | False |  |
| B08Rules.Resume | controlled | NOT_RUN |  | False | Dependency failed: B08Rules.Run |
| B08Rules.FinalResume | controlled | FAIL | 1 | False |  |
| B08Rules.CompleteResume | controlled | FAIL | 1 | False |  |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
