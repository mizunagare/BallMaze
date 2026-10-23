// Explicit negative control for the external monitor lifecycle. Never a Unity/Player driver.
System.Console.Error.WriteLine("INTENTIONAL_MONITOR_FAILURE exit=7; no debugger attached, no game state accessed");
return 7;
