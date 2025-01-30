import moteur
import time as t
from position_robot import Position_robot

c = Position_robot((25,25),(0,1))

moteur.setup()

t.sleep(1)

for _ in range(12):
    print(c.get_tick_offset())
    moteur.rota_deg(90,c)
    print(c.get_tick_offset())
