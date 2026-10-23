# Local unattended validation
Root: C:\Users\guan\Documents\unitytest\WanxiangUnattended\20261023-234207-224ccf3e

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| preflight | environment | PASS |  | False | Tools and space available; source/user processes will not be closed |
| probe.nonzero | harness-negative | FAIL | 7 | False |  |
| probe.timeout | harness-negative | FAIL |  | True | Timeout; process preserved. Dependent project stages must skip. |
| probe.after-failure | harness-negative | PASS | 0 | False |  |
| orchestrator.self-check | harness | PASS |  | False | Expected failure retained, timeout diagnosed without kill, independent next task ran |
| native-worker.build | tool | PASS | 0 | False |  |
| prepare | tool | PASS | 0 | False |  |
| WGAssetAudit.Run | controlled | PASS | 0 | False |  |
| T06RegContainerRuntimeCheck.Run | controlled | PASS | 0 | False |  |
| T06RegDualWeaponCheck.Run | controlled | PASS | 0 | False |  |
| T06RegWorkbenchCheck.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Resume | controlled | PASS | 0 | False |  |
| WGB1Routes.Run | controlled | PASS | 0 | False |  |
| B06ForestCheck.Run | controlled | PASS | 0 | False |  |
| WGA1Check.Isolation | controlled | PASS | 0 | False |  |
| WGA1Check.Choice | controlled | PASS | 0 | False |  |
| WGA1Check.Empty | controlled | PASS | 0 | False |  |
| WGA1Check.Recovery | controlled | PASS | 0 | False |  |
| UI01Rules.Run | controlled | PASS | 0 | False |  |
| U16Fixture.Run | controlled | PASS | 0 | False |  |
| WanxiangBuild.ValidateBuild | controlled | PASS | 0 | False |  |
| normal-ai.Normal | normal-ai | FAIL | 1 | False |  |
| normal-ai.Resume | normal-ai | NOT_RUN |  | False | Normal AI did not finish |
| controlled.visual | controlled-visual | PASS | 0 | False |  |
| player.Default-1.1 | native-close | FAIL |  | False | Timeout: preserved owned process and snapshot; no forced normal-exit PASS |
| analyze.Default-2.1 | native-close | PASS | 0 | False |  |
| player.Default-2.2 | native-close | FAIL |  | False | Timeout: preserved owned process and snapshot; no forced normal-exit PASS |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
