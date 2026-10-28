# Local unattended validation
Root: I:\WCR1\1028-112303-d255ec\Close3

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| pure-release-title | formal-release | PASS |  | False | Actual bit-identical pure release; no runtime acceptance driver |
| independent-exit-observer | exit-observer | PASS | 0 | False |  |
| child-native-exit | formal-release-exit | PASS |  | False | Retained handle signaled=True, actual code=0; PID disappearance is not proof |
| host-native-exit | exit-observer | PASS |  | False | Separate host signal=True, code=0 |
| title-quit-audit | formal-release-exit | PASS |  | False | Independent product OnApplicationQuit audit; queued request alone is insufficient |
| shutdown-log | formal-release-exit | PASS |  | False | Full log archived; absence here does not resolve historical D3D12 root cause |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
