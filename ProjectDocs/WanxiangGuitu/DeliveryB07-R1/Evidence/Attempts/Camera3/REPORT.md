# Local unattended validation
Root: D:/WanxiangValidationRuns/B07R1CameraDiagnostic3

| Stage | Scope | Status | Exit | Timeout | Reason |
|---|---|---|---|---|---|
| B07ReadabilityVisual.Diagnose | controlled-diagnostic | FAIL |  | False | System.Management.Automation.MethodInvocationException: Exception calling "Start" with "1" argument(s): "Cannot start process because a file name has not been provided."   ---> System.InvalidOperationException: Cannot start process because a file name has not been provided.     at System.Diagnostics.Process.Start()     at System.Diagnostics.Process.Start(ProcessStartInfo startInfo)     at CallSite.Target(Closure, CallSite, Type, Object)     --- End of inner exception stack trace ---     at System.Management.Automation.ExceptionHandlingOps.CheckActionPreference(FunctionContext funcContext, Exception exception)     at System.Management.Automation.Interpreter.ActionCallInstruction`2.Run(InterpretedFrame frame)     at System.Management.Automation.Interpreter.EnterTryCatchFinallyInstruction.Run(InterpretedFrame frame)     at System.Management.Automation.Interpreter.EnterTryCatchFinallyInstruction.Run(InterpretedFrame frame) |

Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.
