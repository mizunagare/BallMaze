# Local unattended validation
Root: D:\WanxiangValidationRuns\B08Directed2\20261025-172123-1201d04e

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| B08Probe.Run | controlled | PASS | 0 | False |  |
| B08Rules.Run | controlled | FAIL | 1 | False |  |
| B08Rules.Resume | controlled | NOT_RUN |  | False | Dependency failed: B08Rules.Run |
| B08Rules.FinalResume | controlled | NOT_RUN |  | False | Dependency failed: B08Rules.Resume |
| B08Rules.CompleteResume | controlled | NOT_RUN |  | False | Dependency failed: B08Rules.FinalResume |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
