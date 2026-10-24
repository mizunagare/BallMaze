# Local unattended validation
Root: D:\WanxiangValidationRuns\B07Directed3\20261024-224657-2d07d44f

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| B07Probe.Run | controlled | FAIL | 1 | False |  |
| B07Rules.Run | controlled | NOT_RUN |  | False | Compilation failed in this isolated copy |
| B07Rules.Resume | controlled | NOT_RUN |  | False | Dependency failed: B07Rules.Run |
| B07Rules.PendingResume | controlled | NOT_RUN |  | False | Dependency failed: B07Rules.Resume |
| B07Rules.CommittedResume | controlled | NOT_RUN |  | False | Dependency failed: B07Rules.PendingResume |
| B07Combat.Run | controlled | NOT_RUN |  | False | Compilation failed in this isolated copy |
| B07Economy.Run | controlled | NOT_RUN |  | False | Compilation failed in this isolated copy |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
