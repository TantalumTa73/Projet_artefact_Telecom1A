import controller as c

def action_moteur(type_action):

    if type_action[0] == "r":

        dist = int(type_action[1:])
        