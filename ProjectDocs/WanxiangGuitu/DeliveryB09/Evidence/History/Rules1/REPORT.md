# Local unattended validation
Root: D:\WanxiangValidationRuns\B09Rules1\20261025-204410-96a235a1

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| B09Probe.Run | controlled | FAIL | 1 | False |  |
| B09Rules.Run | controlled | NOT_RUN |  | False | Compilation failed in this isolated copy |
| B09Rules.Resume | controlled | NOT_RUN |  | False | Dependency failed: B09Rules.Run |
| B09Rules.Interrupt | controlled | NOT_RUN |  | False | Compilation failed in this isolated copy |
| B09Rules.Recover | controlled | NOT_RUN |  | False | Compilation failed in this isolated copy |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
