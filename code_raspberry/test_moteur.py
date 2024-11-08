import moteur
import sys

# Access the argument from the command line
if len(sys.argv) > 1:
    arg = sys.argv[1]
    print(f"Received argument: {arg}")
else:
    print("No argument provided")

for inst in arg:

    moteur.action_moteur(inst)