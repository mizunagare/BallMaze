# Local unattended validation
Root: C:\Users\guan\Documents\unitytest\WanxiangUnattended\20261023-235913-583d98d8

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| preflight | environment | PASS |  | False | Tools and space available; source/user processes will not be closed |
| probe.nonzero | harness-negative | FAIL | 7 | False |  |
| probe.timeout | harness-negative | FAIL |  | True | Timeout; process preserved. Dependent project stages must skip. |
| probe.after-failure | harness-negative | PASS | 0 | False |  |
| orchestrator.self-check | harness | PASS |  | False | Expected failure retained, timeout diagnosed without kill, independent next task ran |
| native-worker.build | tool | PASS | 0 | False |  |
| worker.safe-input-rejection | native-ui | NOT_RUN | 3 | False |  |
| worker.normal-close | harness | PASS | 0 | False |  |
| worker.private-desktop-self-check | harness | PASS |  | False | Synthetic worker only: inactive desktop, zero input, owned normal close, actual exit0. Not U16. |
| prepare | tool | PASS | 0 | False |  |
| shader-cache | environment | PASS |  | False | Copied matching-version shader cache read-only; not a clean shader-compilation claim |
| WGRoutesCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B06V8MigrationCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05ScenarioCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05LegacyMigrationCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05V7MigrationCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05LiveRegression.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| T06RegContainerRuntimeCheck.Final | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGPotionCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05EditChecks.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGDeliveryACheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGLegacyForestCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.Matrix | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.InterruptedWrite | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.InterruptedResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGAssetAudit.Run | controlled | PASS | 0 | False |  |
| T06RegContainerRuntimeCheck.Run | controlled | PASS | 0 | False |  |
| T06RegDualWeaponCheck.Run | controlled | PASS | 0 | False |  |
| T06RegWorkbenchCheck.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Resume | controlled | PASS | 0 | False |  |
| WGB1Routes.Run | controlled | PASS | 0 | False |  |
| B06ForestCheck.Run | controlled | PASS | 0 | False |  |
| B06DropCheck.Run | controlled | PASS | 0 | False |  |
| B05FaultCheck.Run | controlled | PASS | 0 | False |  |
| WGA1Check.Isolation | controlled | PASS | 0 | False |  |
| WGA1Check.Choice | controlled | PASS | 0 | False |  |
| WGA1Check.Empty | controlled | PASS | 0 | False |  |
| WGA1Check.Recovery | controlled | PASS | 0 | False |  |
| UI01Rules.Run | controlled | PASS | 0 | False |  |
| U16Fixture.Run | controlled | PASS | 0 | False |  |
| WanxiangBuild.ValidateBuild | controlled | PASS | 0 | False |  |
| normal-ai.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Resume | normal-ai | PASS | 0 | False |  |
| controlled.visual | controlled-visual | PASS | 0 | False |  |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
