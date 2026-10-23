# Local unattended validation
Root: C:\Users\guan\Documents\unitytest\WanxiangUnattended\20261024-014249-0bc58152

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| preflight | environment | PASS |  | False | Tools and space available; source/user processes will not be closed |
| probe.nonzero | harness-negative | FAIL | 7 | False |  |
| probe.timeout | harness-negative | FAIL |  | True | Timeout; process preserved. Dependent project stages must skip. |
| probe.after-failure | harness-negative | PASS | 0 | False |  |
| orchestrator.self-check | harness | PASS |  | False | Expected failure retained, timeout diagnosed without kill, independent next task ran |
| orchestrator.utc-self-check | harness | PASS |  | False | ISO JSON date/object boundary compared in UTC, never DateTime versus formatted string |
| native-worker.build | tool | PASS | 0 | False |  |
| worker.safe-input-rejection | native-ui | NOT_RUN | 3 | False |  |
| worker.normal-close | harness | PASS | 0 | False |  |
| worker.private-desktop-self-check | harness | PASS |  | False | Synthetic worker only: inactive desktop, zero input, owned normal close, actual exit0. Not U16. |
| reuse.build-fixture | artifact | PASS |  | False | Owned independent build copied and hashed; other phases NOT_RUN in matrix-only mode |
| rules | suite-selection | NOT_RUN |  | False | Matrix-only invocation; see original run, do not inherit PASS |
| normal-ai | suite-selection | NOT_RUN |  | False | Matrix-only invocation; see original run, do not inherit PASS |
| controlled.visual | suite-selection | NOT_RUN |  | False | Matrix-only invocation; see original run, do not inherit PASS |
| build.hashes | artifact | PASS |  | False | Complete independent Release file manifest; applies to every Player command in this run |
| native.Default-dump.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.Default-dump.1 | native-close | PASS | 0 | False |  |
| dump-validation.Default-dump | diagnostic | FAIL | 1 | False |  |
| dump.Default-dump | diagnostic | FAIL | 7 | False | Raw exit retained; classification requires signed pinned binary, calibrated exit/count and structurally valid completed dumps; see dump-validation.json |
| analyze.Default-dump.1 | native-close | PASS | 0 | False |  |
| U16.Default-dump.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| shutdown.root-cause | diagnostic | UNRESOLVED |  | False | Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence. |
| human-usability | human | NOT_RUN |  | False | Requires independent real human judgment; never substituted by automation |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
