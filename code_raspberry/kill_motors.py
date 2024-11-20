import controller
import time
c = controller.Controller()
print("Shutting down motors...", end="")
c.set_motor_speed(0,0)
print("OK")

print("Reseting motors...", end="")
c.reset()
print("OK")
time.sleep(2)
