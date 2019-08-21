import random

from sismic.interpreter import Interpreter
from sismic.io import import_from_yaml

from statecharts.crypto_token_statechart import crypto_token_statechart
from statecharts.passwords_statechart import passwords_statechart


def random_tests(elevator, has_error_in_context):
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
        # TODO: with help of contracts
        if has_error_in_context(interpreter):
            print('ERRORR!')
            exit(1)

    print('After:', interpreter.configuration)


# random_tests(passwords_statechart,
#              lambda interpreter: interpreter.context['pin_count'] < 0)
random_tests(crypto_token_statechart, lambda interpreter: False)
