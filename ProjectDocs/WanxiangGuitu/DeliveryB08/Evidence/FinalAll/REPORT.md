# Local unattended validation
Root: D:\WanxiangValidationRuns\B08ReleaseAll\20261025-190134-7b35aac0

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
| WGB1Check.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Resume | controlled | PASS | 0 | False |  |
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
| B4StateRules.Run | controlled | PASS | 0 | False |  |
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
| B07SeedReplay.Run | controlled | PASS | 0 | False |  |
| B07Rules.Run | controlled | PASS | 0 | False |  |
| B07Rules.Resume | controlled | PASS | 0 | False |  |
| B07Rules.PendingResume | controlled | PASS | 0 | False |  |
| B07Rules.CommittedResume | controlled | PASS | 0 | False |  |
| B07Combat.Run | controlled | PASS | 0 | False |  |
| B07Interruptions.Run | controlled | PASS | 0 | False |  |
| B07Economy.Run | controlled | PASS | 0 | False |  |
| B07Liveness.Run | controlled | PASS | 0 | False |  |
| B07ReadabilityProbe.Run | controlled | PASS | 0 | False |  |
| B07ReadabilityRules.Run | controlled | PASS | 0 | False |  |
| B07ReadabilityVisual.Run | controlled | PASS | 0 | False |  |
| B07OcclusionProbe.Run | controlled | PASS | 0 | False |  |
| B07ActorOcclusion.Run | controlled | PASS | 0 | False |  |
| B08Probe.Run | controlled | PASS | 0 | False |  |
| B08Rules.Run | controlled | PASS | 0 | False |  |
| B08Rules.Resume | controlled | PASS | 0 | False |  |
| B08Rules.FinalResume | controlled | PASS | 0 | False |  |
| B08Rules.CompleteResume | controlled | PASS | 0 | False |  |
| B08Recovery.Run | controlled | PASS | 0 | False |  |
| B08Recovery.Resume | controlled | PASS | 0 | False |  |
| B08CampPause.Run | controlled | PASS | 0 | False |  |
| B08Visual.Run | controlled | PASS | 0 | False |  |
| U16Fixture.Run | controlled | PASS | 0 | False |  |
| WanxiangBuild.ValidateBuild | controlled | PASS | 0 | False |  |
| normal-ai.Gather.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Gather.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Gather.FinalResume | normal-ai | PASS | 0 | False |  |
| normal-ai.Treasure.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Treasure.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Treasure.FinalResume | normal-ai | PASS | 0 | False |  |
| normal-ai.Bypass.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Bypass.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Bypass.FinalResume | normal-ai | PASS | 0 | False |  |
| normal-ai.Land.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Land.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Land.FinalResume | normal-ai | PASS | 0 | False |  |
| normal-ai.Lake.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Lake.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Lake.FinalResume | normal-ai | PASS | 0 | False |  |
| normal-ai.Tutorial.Normal | normal-ai | PASS | 0 | False |  |
| normal-ai.Tutorial.Resume | normal-ai | PASS | 0 | False |  |
| normal-ai.Tutorial.FinalResume | normal-ai | PASS | 0 | False |  |
| controlled.terrain | controlled-visual | PASS | 0 | False |  |
| controlled.visual | controlled-visual | PASS | 0 | False |  |
| build.hashes | artifact | PASS |  | False | Complete independent Release file manifest; applies to every Player command in this run |
| native.Default-1.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.Default-1.1 | native-close | PASS | 0 | False |  |
| analyze.Default-1.1 | native-close | PASS | 0 | False |  |
| U16.Default-1.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.Default-1.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.Default-1.2 | native-close | PASS | 0 | False |  |
| analyze.Default-1.2 | native-close | PASS | 0 | False |  |
| U16.Default-1.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.Default-2.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.Default-2.1 | native-close | PASS | 0 | False |  |
| analyze.Default-2.1 | native-close | PASS | 0 | False |  |
| U16.Default-2.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.Default-2.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.Default-2.2 | native-close | PASS | 0 | False |  |
| analyze.Default-2.2 | native-close | PASS | 0 | False |  |
| U16.Default-2.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.D3D11-1.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.D3D11-1.1 | native-close | PASS | 0 | False |  |
| analyze.D3D11-1.1 | native-close | PASS | 0 | False |  |
| U16.D3D11-1.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.D3D11-1.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.D3D11-1.2 | native-close | PASS | 0 | False |  |
| analyze.D3D11-1.2 | native-close | PASS | 0 | False |  |
| U16.D3D11-1.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.D3D11-2.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.D3D11-2.1 | native-close | PASS | 0 | False |  |
| analyze.D3D11-2.1 | native-close | PASS | 0 | False |  |
| U16.D3D11-2.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.D3D11-2.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.D3D11-2.2 | native-close | PASS | 0 | False |  |
| analyze.D3D11-2.2 | native-close | PASS | 0 | False |  |
| U16.D3D11-2.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| matrix.Default-dump | diagnostic | NOT_RUN |  | False | Optional ProcDump unavailable; non-monitored cells unaffected |
| native.B07-Land.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.B07-Land.1 | native-close | PASS | 0 | False |  |
| analyze.B07-Land.1 | native-close | PASS | 0 | False |  |
| B07-Player.B07-Land.1 | player-smoke | PASS | 0 | False |  |
| U16.B07-Land.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.B07-Land.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.B07-Land.2 | native-close | PASS | 0 | False |  |
| analyze.B07-Land.2 | native-close | PASS | 0 | False |  |
| B07-Player.B07-Land.2 | player-smoke | PASS | 0 | False |  |
| U16.B07-Land.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.B07-Lake.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.B07-Lake.1 | native-close | PASS | 0 | False |  |
| analyze.B07-Lake.1 | native-close | PASS | 0 | False |  |
| B07-Player.B07-Lake.1 | player-smoke | PASS | 0 | False |  |
| U16.B07-Lake.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.B07-Lake.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.B07-Lake.2 | native-close | PASS | 0 | False |  |
| analyze.B07-Lake.2 | native-close | PASS | 0 | False |  |
| B07-Player.B07-Lake.2 | player-smoke | PASS | 0 | False |  |
| U16.B07-Lake.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.B08-Tutorial.1 | native-ui | NOT_RUN | 3 | False |  |
| close-request.B08-Tutorial.1 | native-close | PASS | 0 | False |  |
| analyze.B08-Tutorial.1 | native-close | PASS | 0 | False |  |
| B08-Player.B08-Tutorial.1 | player-smoke | PASS | 0 | False |  |
| U16.B08-Tutorial.1 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| native.B08-Tutorial.2 | native-ui | NOT_RUN | 3 | False |  |
| close-request.B08-Tutorial.2 | native-close | PASS | 0 | False |  |
| analyze.B08-Tutorial.2 | native-close | PASS | 0 | False |  |
| B08-Player.B08-Tutorial.2 | player-smoke | PASS | 0 | False |  |
| U16.B08-Tutorial.2 | native-ui | NOT_RUN |  | False | Player not foreground/visible; no activation, global hotkey or input sent |
| shutdown.root-cause | diagnostic | UNRESOLVED |  | False | Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence. |
| render.first-frame-root-cause | diagnostic | UNRESOLVED |  | False | Earlier controlled Editor captures briefly showed solid cyan; stable-frame captures have a separate pixel assertion. Internal cause not proven; no product lifecycle or renderer patch inferred. |
| human-usability | human | NOT_RUN |  | False | Requires independent real human judgment; never substituted by automation |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
