import math
from domination import core
from domination import run

FIELD = """
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ w _ C _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ w _ _ _ w w w w w w w w w w w _ _ _ _ _ _ w
w _ _ w _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ w
w R _ w _ _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ B w
w R _ w _ _ _ w _ A _ _ w w w w w _ _ A _ w _ _ _ w _ B w
w R _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ w _ B w
w _ _ w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ w _ _ w
w _ _ _ _ _ _ w w w w w w w w w w w _ _ _ w _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ C _ w _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ w
w w w w w w w w w w w w w w w w w w w w w w w w w w w w w
"""

class Tournament1(run.Scenario):
    GENERATOR = None
    FIELD     = core.Field.from_string(FIELD)
    SETTINGS  = core.Settings(ammo_amount=1, 
                              spawn_time=10, 
                              ammo_rate=9, 
                              max_see=70,
                              think_time=0.06,
                              max_turn=math.pi/4,
                              max_score=10000)


#Tournament1.one_on_one(red="domination/agent.py", blue="retardedAgent.py", output_folder='_tmp')<<<<<<< HEAD
Tournament1.test(red="agents/retardedAgent_old.py", blue="agents/retardedAgent.py")
#Tournament1.test(red="tzak.py", blue="retardedAgent.py")

