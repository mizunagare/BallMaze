# Local unattended validation
Root: C:\Users\guan\Documents\unitytest\WanxiangB2\20261024-030559-22e783b6

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
| WGA1ExtendedCheck.Matrix | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.InterruptedWrite | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.InterruptedResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B2Rules.Run | controlled | PASS | 0 | False |  |
| B2Rules.Resume | controlled | PASS | 0 | False |  |
| WGAssetAudit.Run | controlled | PASS | 0 | False |  |
| T06RegContainerRuntimeCheck.Run | controlled | PASS | 0 | False |  |
| T06RegDualWeaponCheck.Run | controlled | PASS | 0 | False |  |
| T06RegWorkbenchCheck.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Resume | controlled | PASS | 0 | False |  |
| WGB1Routes.Run | controlled | PASS | 0 | False |  |
| WGLegacyForestCheck.Run | controlled | PASS | 0 | False |  |
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
| build.hashes | artifact | PASS |  | False | Complete independent Release file manifest; applies to every Player command in this run |
| player-matrix | native-close | NOT_RUN |  | False | GameplayOnly: shutdown diagnostic matrix intentionally not repeated; historical evidence retained |
| U16.native | native-ui | NOT_RUN |  | False | No authorized independent interactive environment; gameplay checks and controlled screenshots are not native UI acceptance |
| shutdown.root-cause | diagnostic | UNRESOLVED |  | False | Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence. |
| human-usability | human | NOT_RUN |  | False | Requires independent real human judgment; never substituted by automation |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
