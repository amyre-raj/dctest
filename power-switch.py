import dlipower 

print("Connecting to a DLI PowerSwitch at lpc.digital-loggers.com")
switch = dlipower.PowerSwitch(hostname="lpc.digital-loggers.com", userid="admin")

print("Turning off the first outlet")
switch.off(1)

print("The powerstate of the first outlet is currently", switch[0].state)