# Local unattended validation
Root: D:\WanxiangValidationRuns\B10PlayerControl3

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| prepare | tool | PASS | 0 | False |  |
| controller.prepare | controlled-build | PASS | 0 | False |  |
| controller.build | controlled-build | PASS | 0 | False |  |
| player.read | controlled-player | FAIL | 3 | False |  |
| player.read.receipt | controlled-player | FAIL |  | False | Missing/failed completion receipt or abnormal/timeout exit; no kill |
| player.continue | controlled-player | NOT_RUN |  | False | First process failed; do not claim resume |
| player.new | controlled-player | PASS | 0 | False |  |
| player.new.receipt | controlled-player | PASS |  | False | Actual self exit0 and real uGUI callbacks completed; no native input claim |
| player.pending | controlled-player | PASS | 0 | False |  |
| player.pending.receipt | controlled-player | PASS |  | False | Actual self exit0 and real uGUI callbacks completed; no native input claim |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
