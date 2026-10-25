# Local unattended validation
Root: D:\WanxiangValidationRuns\B09ReleaseFinal\20261025-221755-dd51d1a4

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| preflight | environment | PASS |  | False | Tools and space available; source/user processes will not be closed |
| probe.nonzero | harness-negative | FAIL | 7 | False |  |
| probe.timeout | harness-negative | FAIL |  | True | Timeout; process preserved. Dependent project stages must skip. |
| probe.after-failure | harness-negative | PASS | 0 | False |  |
| orchestrator.self-check | harness | PASS |  | False | Expected failure retained, timeout diagnosed without kill, independent next task ran |
| orchestrator.report-reader-lock | harness | PASS |  | False | Independent read lock released; bounded atomic report publication retried; old JSON remained intact. No test/product failure reclassification. |
| orchestrator.utc-self-check | harness | PASS |  | False | ISO JSON date/object boundary compared in UTC, never DateTime versus formatted string |
| worker.no-direct-unity | harness | PASS |  | False | Unity basename requires private worker even without UnityPath binding; missing executable probe starts no process |
| native-worker.build | tool | PASS | 0 | False |  |
| worker.safe-input-rejection | native-ui | NOT_RUN | 3 | False |  |
| worker.normal-close | harness | PASS | 0 | False |  |
| worker.private-desktop-self-check | harness | PASS |  | False | Synthetic worker only: inactive desktop, zero input, owned normal close, actual exit0. Not U16. |
| prepare | tool | PASS | 0 | False |  |
| shader-cache | environment | PASS |  | False | Copied matching-version shader cache read-only; not a clean shader-compilation claim |
| WGAssetAudit.Run | controlled | FAIL | 1 | False |  |
| WGRoutesCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B06DropCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B06V8MigrationCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B05ScenarioCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B05FaultCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B05LegacyMigrationCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B05V7MigrationCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B05LiveRegression.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| T06RegContainerRuntimeCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| T06RegContainerRuntimeCheck.Final | controlled | NOT_RUN |  | False | Dependency did not pass: T06RegContainerRuntimeCheck.Run |
| T06RegDualWeaponCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| T06RegWorkbenchCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGPotionCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B05EditChecks.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGB1Check.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGB1Check.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: WGB1Check.Run |
| WGB1Routes.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGDeliveryACheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGLegacyForestCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B06ForestCheck.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| RouteScoringProbe.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| RouteScoringRules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| RouteScoringRules.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: RouteScoringRules.Run |
| R1Audit.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| R1Shore.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| R1Rules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| R1Rules.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: R1Rules.Run |
| B4Checks.Topology | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B4Physics.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B4StateRules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B4PickupRules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B3StreamRules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B3Checks.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B3Checks.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: B3Checks.Run |
| B2Rules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B2Rules.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: B2Rules.Run |
| WGA1Check.Isolation | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGA1Check.Choice | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGA1Check.Empty | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGA1Check.Recovery | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGA1ExtendedCheck.Matrix | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGA1ExtendedCheck.InterruptedWrite | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WGA1ExtendedCheck.InterruptedResume | controlled | NOT_RUN |  | False | Dependency did not pass: WGA1ExtendedCheck.InterruptedWrite |
| UI01Rules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07Probe.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07SeedReplay.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07Rules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07Rules.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: B07Rules.Run |
| B07Rules.PendingResume | controlled | NOT_RUN |  | False | Dependency did not pass: B07Rules.Resume |
| B07Rules.CommittedResume | controlled | NOT_RUN |  | False | Dependency did not pass: B07Rules.PendingResume |
| B07Combat.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07Interruptions.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07Economy.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07Liveness.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07ReadabilityProbe.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07ReadabilityRules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07ReadabilityVisual.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07OcclusionProbe.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B07ActorOcclusion.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B08Probe.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B08Rules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B08Rules.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: B08Rules.Run |
| B08Rules.FinalResume | controlled | NOT_RUN |  | False | Dependency did not pass: B08Rules.Resume |
| B08Rules.CompleteResume | controlled | NOT_RUN |  | False | Dependency did not pass: B08Rules.FinalResume |
| B08Recovery.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B08Recovery.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: B08Recovery.Run |
| B08CampPause.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B08Visual.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B09Probe.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B09Rules.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B09Rules.Resume | controlled | NOT_RUN |  | False | Dependency did not pass: B09Rules.Run |
| B09Rules.Interrupt | controlled | NOT_RUN |  | False | Dependency did not pass: B09Rules.Resume |
| B09Rules.Recover | controlled | NOT_RUN |  | False | Dependency did not pass: B09Rules.Interrupt |
| B09Preferences.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B09Cases.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| B09Cases.Pending | controlled | NOT_RUN |  | False | Dependency did not pass: B09Cases.Run |
| B09Cases.Committed | controlled | NOT_RUN |  | False | Dependency did not pass: B09Cases.Run |
| B09Visual.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| U16Fixture.Run | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| WanxiangBuild.ValidateBuild | controlled | NOT_RUN |  | False | Compilation dependency failed; do not repeat identical compiler failure |
| normal-ai.Gather.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Gather.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Gather.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Treasure.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Treasure.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Treasure.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Bypass.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Bypass.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Bypass.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Land.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Land.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Land.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Lake.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Lake.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Lake.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Tutorial.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Tutorial.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Tutorial.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Entry.Normal | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Entry.Resume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| normal-ai.Entry.FinalResume | normal-ai | NOT_RUN |  | False | Isolated Editor occupied or compile/desktop dependency blocked |
| controlled.terrain | controlled-visual | NOT_RUN |  | False | Isolated visual dependency unavailable |
| controlled.visual | controlled-visual | NOT_RUN |  | False | Isolated Editor/compile/desktop dependency blocked |
| player-matrix | native-close | NOT_RUN |  | False | GameplayOnly: shutdown diagnostic matrix intentionally not repeated; historical evidence retained |
| U16.native | native-ui | NOT_RUN |  | False | No authorized independent interactive environment; gameplay checks and controlled screenshots are not native UI acceptance |
| shutdown.root-cause | diagnostic | UNRESOLVED |  | False | Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence. |
| render.first-frame-root-cause | diagnostic | UNRESOLVED |  | False | Earlier controlled Editor captures briefly showed solid cyan; stable-frame captures have a separate pixel assertion. Internal cause not proven; no product lifecycle or renderer patch inferred. |
| human-usability | human | NOT_RUN |  | False | Requires independent real human judgment; never substituted by automation |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
