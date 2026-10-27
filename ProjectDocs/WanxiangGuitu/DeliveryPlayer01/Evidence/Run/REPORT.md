# Local unattended validation
Root: D:\WGP01\1027-195130-818e8dee

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| formal-gather-capability | formal-player-adventure | NOT_RUN |  | False | Gather and resume use UnityEditor/A1ValidationDrivers and -executeMethod; final Player strips these. No formal Player AI injection or gameplay bypass will be added. |
| formal-settings-input-capability | formal-player-input | NOT_RUN |  | False | No authorized independent interactive input desktop. Existing virtual InputSystem and uGUI test driver is Editor-only. |
| Input01Rules.Run | editor-controlled | PASS | 0 | False |  |
| Input01Play.Run | editor-controlled | PASS | 0 | False |  |
| Input01Play.Resume | editor-controlled | PASS | 0 | False |  |
| B09Rules.Run | editor-controlled | PASS | 0 | False |  |
| B09Rules.Resume | editor-controlled | PASS | 0 | False |  |
| B09Rules.Interrupt | editor-controlled | PASS | 0 | False |  |
| B09Rules.Recover | editor-controlled | PASS | 0 | False |  |
| B09Cases.Run | editor-controlled | PASS | 0 | False |  |
| B09Cases.Pending | editor-controlled | PASS | 0 | False |  |
| B09Cases.Committed | editor-controlled | PASS | 0 | False |  |
| U16Fixture.Run | editor-controlled | PASS | 0 | False |  |
| P01Confirmation.Run | editor-controlled | PASS | 0 | False |  |
| Gather.Normal | editor-normal-ai | PASS | 0 | False |  |
| Gather.Resume | editor-normal-ai | PASS | 0 | False |  |
| Gather.FinalResume | editor-normal-ai | PASS | 0 | False |  |
| native-environment-check | native-ui | NOT_RUN | 3 | False |  |
| PlayerClose.Missing | native-close | PASS | 0 | False |  |
| PlayerVerify.Missing | formal-player | PASS | 0 | False |  |
| PlayerClose.Ready | native-close | PASS | 0 | False |  |
| PlayerVerify.Ready | formal-player | PASS | 0 | False |  |
| PlayerClose.Corrupt | native-close | PASS | 0 | False |  |
| PlayerVerify.Corrupt | formal-player | PASS | 0 | False |  |
| PlayerClose.Incompatible | native-close | PASS | 0 | False |  |
| PlayerVerify.Incompatible | formal-player | PASS | 0 | False |  |
| PlayerClose.Pending | native-close | PASS | 0 | False |  |
| PlayerVerify.Pending | formal-player | PASS | 0 | False |  |
| PlayerClose.Committed | native-close | PASS | 0 | False |  |
| PlayerVerify.Committed | formal-player | PASS | 0 | False |  |
| native-U16-human | native-human | NOT_RUN |  | False | No independent interactive desktop/tester; no switching or activation allowed |
| full-performance | performance | NOT_RUN |  | False | No fixed gameplay load accessible in final Player automation. Startup/screenshots are not a performance benchmark. |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
