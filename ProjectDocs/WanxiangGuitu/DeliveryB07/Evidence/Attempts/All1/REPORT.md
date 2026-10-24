# Local unattended validation
Root: D:\WanxiangValidationRuns\B07All\20261024-233120-dd7c8b86

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| preflight | environment | PASS |  | False | Tools and space available; source/user processes will not be closed |
| probe.nonzero | harness-negative | FAIL | 7 | False |  |
| probe.timeout | harness-negative | FAIL |  | True | Timeout; process preserved. Dependent project stages must skip. |
| probe.after-failure | harness-negative | PASS | 0 | False |  |
| orchestrator.self-check | harness | PASS |  | False | Expected failure retained, timeout diagnosed without kill, independent next task ran |
| orchestrator.utc-self-check | harness | PASS |  | False | ISO JSON date/object boundary compared in UTC, never DateTime versus formatted string |
| worker.no-direct-unity | harness | PASS |  | False | Unity basename requires private worker even without UnityPath binding; missing executable probe starts no process |
| native-worker.build | tool | PASS | 0 | False |  |
| worker.safe-input-rejection | native-ui | NOT_RUN | 3 | False |  |
| worker.normal-close | harness | PASS | 0 | False |  |
| worker.private-desktop-self-check | harness | PASS |  | False | Synthetic worker only: inactive desktop, zero input, owned normal close, actual exit0. Not U16. |
| prepare | tool | PASS | 0 | False |  |
| shader-cache | environment | PASS |  | False | Copied matching-version shader cache read-only; not a clean shader-compilation claim |
| WGAssetAudit.Run | controlled | PASS | 0 | False |  |
| WGRoutesCheck.Run | controlled | PASS | 0 | False |  |
| B06DropCheck.Run | controlled | PASS | 0 | False |  |
| B06V8MigrationCheck.Run | controlled | PASS | 0 | False |  |
| B05ScenarioCheck.Run | controlled | PASS | 0 | False |  |
| B05FaultCheck.Run | controlled | PASS | 0 | False |  |
| B05LegacyMigrationCheck.Run | controlled | PASS | 0 | False |  |
| B05V7MigrationCheck.Run | controlled | PASS | 0 | False |  |
| B05LiveRegression.Run | controlled | PASS | 0 | False |  |
| T06RegContainerRuntimeCheck.Run | controlled | PASS | 0 | False |  |
| T06RegContainerRuntimeCheck.Final | controlled | PASS | 0 | False |  |
| T06RegDualWeaponCheck.Run | controlled | PASS | 0 | False |  |
| T06RegWorkbenchCheck.Run | controlled | PASS | 0 | False |  |
| WGPotionCheck.Run | controlled | PASS | 0 | False |  |
| B05EditChecks.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Run | controlled | FAIL | 1 | False |  |
| WGB1Check.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: WGB1Check.Run |
| WGB1Routes.Run | controlled | PASS | 0 | False |  |
| WGDeliveryACheck.Run | controlled | PASS | 0 | False |  |
| WGLegacyForestCheck.Run | controlled | PASS | 0 | False |  |
| B06ForestCheck.Run | controlled | PASS | 0 | False |  |
| RouteScoringProbe.Run | controlled | PASS | 0 | False |  |
| RouteScoringRules.Run | controlled | PASS | 0 | False |  |
| RouteScoringRules.Resume | controlled | PASS | 0 | False |  |
| R1Audit.Run | controlled | PASS | 0 | False |  |
| R1Shore.Run | controlled | PASS | 0 | False |  |
| R1Rules.Run | controlled | PASS | 0 | False |  |
| R1Rules.Resume | controlled | PASS | 0 | False |  |
| B4Checks.Topology | controlled | PASS | 0 | False |  |
| B4Physics.Run | controlled | PASS | 0 | False |  |
| B4StateRules.Run | controlled | FAIL | 1 | False |  |
| B4PickupRules.Run | controlled | PASS | 0 | False |  |
| B3StreamRules.Run | controlled | PASS | 0 | False |  |
| B3Checks.Run | controlled | PASS | 0 | False |  |
| B3Checks.Resume | controlled | PASS | 0 | False |  |
| B2Rules.Run | controlled | PASS | 0 | False |  |
| B2Rules.Resume | controlled | PASS | 0 | False |  |
| WGA1Check.Isolation | controlled | PASS | 0 | False |  |
| WGA1Check.Choice | controlled | PASS | 0 | False |  |
| WGA1Check.Empty | controlled | PASS | 0 | False |  |
| WGA1Check.Recovery | controlled | PASS | 0 | False |  |
| WGA1ExtendedCheck.Matrix | controlled | PASS | 0 | False |  |
| WGA1ExtendedCheck.InterruptedWrite | controlled | PASS | 0 | False |  |
| WGA1ExtendedCheck.InterruptedResume | controlled | PASS | 0 | False |  |
| UI01Rules.Run | controlled | PASS | 0 | False |  |
| B07Probe.Run | controlled | PASS | 0 | False |  |
| B07Rules.Run | controlled | PASS | 0 | False |  |
| B07Rules.Resume | controlled | PASS | 0 | False |  |
| B07Rules.PendingResume | controlled | PASS | 0 | False |  |
| B07Rules.CommittedResume | controlled | PASS | 0 | False |  |
| B07Combat.Run | controlled | PASS | 0 | False |  |
| B07Economy.Run | controlled | PASS | 0 | False |  |
| B07Liveness.Run | controlled | PASS | 0 | False |  |
| U16Fixture.Run | controlled | PASS | 0 | False |  |
| WanxiangBuild.ValidateBuild | controlled | PASS | 0 | False |  |
| normal-ai.Gather.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Gather.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Gather.FinalResume | normal-ai | PASS | 0 | False |  |
| normal-ai.Treasure.Normal | normal-ai | PASS | 0 | False |  |
| orchestrator.exception | orchestrator | FAIL |  | False | System.IO.IOException: The process cannot access the file 'D:\WanxiangValidationRuns\B07All\20261024-233120-dd7c8b86\results.json' because it is being used by another process.     at System.IO.Strategies.OSFileStreamStrategy..ctor(String path, FileMode mode, FileAccess access, FileShare share, FileOptions options, Int64 preallocationSize, Nullable`1 unixCreateMode)     at Microsoft.PowerShell.Commands.FileSystemProvider.ClearContent(String path) |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
