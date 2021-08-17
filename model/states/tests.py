import random

from sismic.interpreter import Interpreter

from statecharts.e_sign import e_sign_statechart


def random_tests(elevator, has_error_in_context=lambda interpreter: False, precondition=None):
    interpreter = Interpreter(elevator)
    print('Before:', interpreter.configuration)
    if precondition is not None:
        precondition(interpreter)
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
# random_tests(crypto_token_statechart, lambda interpreter: False)


def e_sign_precondition(interpreter):
    interpreter.context['is_authenticated'] = True


random_tests(e_sign_statechart, precondition=e_sign_precondition)
