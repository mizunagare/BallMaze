# Local unattended validation
Root: D:\WanxiangValidationRuns\Input01\20261027-151043-585c2866\DirectedInput2\20261027-154245-6c9d3a52

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| Input01Rules.Run | controlled | PASS | 0 | False |  |
| Input01Play.Run | controlled | FAIL | 1 | False |  |
| Input01Play.Resume | controlled | NOT_RUN |  | False | Dependency failed: Input01Play.Run |
| UI01Rules.Run | controlled | PASS | 0 | False |  |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
