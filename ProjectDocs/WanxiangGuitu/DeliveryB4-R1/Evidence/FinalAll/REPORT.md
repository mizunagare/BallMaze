# Local unattended validation
Root: D:\WanxiangValidationRuns\B4R1Final\20261024-165747-a3f1be5c

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
| WGB1Check.Run | controlled | PASS | 0 | False |  |
| WGB1Check.Resume | controlled | PASS | 0 | False |  |
| WGB1Routes.Run | controlled | PASS | 0 | False |  |
| WGDeliveryACheck.Run | controlled | PASS | 0 | False |  |
| WGLegacyForestCheck.Run | controlled | PASS | 0 | False |  |
| B06ForestCheck.Run | controlled | PASS | 0 | False |  |
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
| shutdown.root-cause | diagnostic | UNRESOLVED |  | False | Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence. |
| human-usability | human | NOT_RUN |  | False | Requires independent real human judgment; never substituted by automation |
| report.finalized | orchestrator | PASS |  | False | Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
