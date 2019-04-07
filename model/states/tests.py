import random

from sismic.interpreter import Interpreter
from sismic.io import import_from_yaml

elevator = import_from_yaml(filepath='passwordBTOK.yml')
interpreter = Interpreter(elevator)
print('Before:', interpreter.configuration)
step = interpreter.execute_once()
print('Step: ', step)
print('Configuration: ', interpreter.configuration)
print('Context: ', interpreter.context)
while step:
    print('_______________________________')
    events = elevator.events_for(interpreter.configuration)
    print('Events: ', events)
    if events:
        next_event = random.randrange(start=0, stop=len(events))
        print('Next event(!!!!!): ', events[next_event])
        interpreter.queue(events[next_event])
    step = interpreter.execute_once()
    print('Step: ', step)
    print('Configuration: ', interpreter.configuration)
    print('Context: ', interpreter.context)
    if interpreter.context['pin_count'] < 0:
        print('ERRORR!')
        exit(1)

print('After:', interpreter.configuration)
