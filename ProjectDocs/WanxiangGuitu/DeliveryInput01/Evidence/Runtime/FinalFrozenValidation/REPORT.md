# Local unattended validation
Root: D:\WanxiangValidationRuns\Input01\20261027-151043-585c2866\FinalFrozenValidation\20261027-161647-ab2a444e

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
| WGAssetAudit.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGRoutesCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B06DropCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B06V8MigrationCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05ScenarioCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05FaultCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05LegacyMigrationCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05V7MigrationCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05LiveRegression.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| T06RegContainerRuntimeCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| T06RegContainerRuntimeCheck.Final | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| T06RegDualWeaponCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| T06RegWorkbenchCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGPotionCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B05EditChecks.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGB1Routes.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGDeliveryACheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGLegacyForestCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B06ForestCheck.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| RouteScoringProbe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| RouteScoringRules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| RouteScoringRules.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| R1Audit.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| R1Shore.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| R1Rules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| R1Rules.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B4Checks.Topology | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B4Physics.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B4StateRules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B4PickupRules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B3Checks.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B3Checks.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1Check.Isolation | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1Check.Choice | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1Check.Empty | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1Check.Recovery | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.Matrix | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.InterruptedWrite | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| WGA1ExtendedCheck.InterruptedResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Probe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07SeedReplay.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Rules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Rules.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Rules.PendingResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Rules.CommittedResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Combat.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Interruptions.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Economy.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07Liveness.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07ReadabilityProbe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07ReadabilityRules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07ReadabilityVisual.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07OcclusionProbe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B07ActorOcclusion.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Probe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Rules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Rules.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Rules.FinalResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Rules.CompleteResume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Recovery.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Recovery.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B08Visual.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Isolation.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Probe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Rules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Rules.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Rules.Interrupt | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Rules.Recover | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Cases.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Cases.Pending | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Cases.Committed | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B09Visual.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10EntryVisual.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10Rules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10Rules.Resume | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10ArtSpec.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10InventoryReadiness.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10Cats.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| B10Comparison.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| Stage2Rules.DamageMetric | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| Stage2Rules.Seeds | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| Stage2Rules.Builds | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| Stage2Rules.RetryBoundary | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| Stage2Physics.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| S2R1ObservationProbe.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| S2R1BoundaryRules.Run | suite-selection | NOT_RUN |  | False | Not selected in focused suite; use -FullRegression; existing regression retained |
| Input01Rules.Run | controlled | PASS | 0 | False |  |
| Input01Play.Run | controlled | PASS | 0 | False |  |
| Input01Play.Resume | controlled | PASS | 0 | False |  |
| B09Preferences.Run | controlled | PASS | 0 | False |  |
| B08CampPause.Run | controlled | PASS | 0 | False |  |
| UI01Rules.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Resume | controlled | PASS | 0 | False |  |
| B2Rules.Run | controlled | PASS | 0 | False |  |
| B2Rules.Resume | controlled | PASS | 0 | False |  |
| B3StreamRules.Run | controlled | PASS | 0 | False |  |
| U16Fixture.Run | controlled | PASS | 0 | False |  |
| WanxiangBuild.ValidateBuild | controlled | PASS | 0 | False |  |
| normal-ai.Gather.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Gather.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Gather.FinalResume | normal-ai | PASS | 0 | False |  |
| controlled.terrain | controlled-visual | NOT_RUN |  | False | Isolated visual dependency unavailable |
| controlled.visual | controlled-visual | NOT_RUN |  | False | Isolated Editor/compile/desktop dependency blocked |
| build.hashes | artifact | PASS |  | False | Complete independent Release file manifest; applies to every Player command in this run |
| B09-RejectVerify.entry-evidence | startup-safety | PASS | 0 | False |  |
| B09-RejectVerify.test-gameplay | startup-safety | PASS | 0 | False |  |
| B09-TitleClose.Missing | native-close | PASS | 0 | False |  |
| B09-TitleVerify.Missing | formal-player | PASS | 0 | False |  |
| B09-TitleClose.Ready | native-close | PASS | 0 | False |  |
| B09-TitleVerify.Ready | formal-player | PASS | 0 | False |  |
| player-matrix | native-close | NOT_RUN |  | False | GameplayOnly: shutdown diagnostic matrix intentionally not repeated; historical evidence retained |
| U16.native | native-ui | NOT_RUN |  | False | No authorized independent interactive environment; gameplay checks and controlled screenshots are not native UI acceptance |
| shutdown.root-cause | diagnostic | UNRESOLVED |  | False | Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence. |
| render.first-frame-root-cause | diagnostic | UNRESOLVED |  | False | Earlier controlled Editor captures briefly showed solid cyan; stable-frame captures have a separate pixel assertion. Internal cause not proven; no product lifecycle or renderer patch inferred. |
| human-usability | human | NOT_RUN |  | False | Requires independent real human judgment; never substituted by automation |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
