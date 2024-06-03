# TODO: Not full
from sismic.model import Statechart, CompoundState, BasicState, Transition

PIN_FLAG = 'is_pin_checked'
AUTH_FLAG = 'is_authenticated'
RESET_PIN = f"{PIN_FLAG} = False"
INIT_PROGRAM = f"{RESET_PIN};{AUTH_FLAG} = False"
INIT_STATE_NAME = 'hibernation'
# n - must be some definite number
EVENTS_TO_RESET_PIN_FLAG = ['keys_generated', 'keys_removed', 'pin_changed', 'n_digital_signature_generated']


def init_hibernation_state(root_state):
    hibernation_state = BasicState(name=INIT_STATE_NAME)
    hibernation_state.invariants = [f"{AUTH_FLAG} == True"]
    e_sign_statechart.add_state(state=hibernation_state, parent=root_state.name)
    add_transitions_to_reset_pin(hibernation_state, create_reset_pin_state(root_state, hibernation_state))


def add_transitions_to_reset_pin(from_state, reset_pin_state):
    for event_name in EVENTS_TO_RESET_PIN_FLAG:
        e_sign_statechart.add_transition(Transition(source=from_state.name,
                                                    target=reset_pin_state.name,
                                                    event=event_name))


def create_reset_pin_state(parent_state, came_from_state):
    reset_pin_state = BasicState(name='Reset Pin',
                                 on_entry=RESET_PIN)
    e_sign_statechart.add_state(state=reset_pin_state, parent=parent_state.name)
    e_sign_statechart.add_transition(Transition(source=reset_pin_state.name,
                                                target=came_from_state.name))
    return reset_pin_state


e_sign_statechart = Statechart(name='eSign states', preamble=INIT_PROGRAM)
root_state = CompoundState(name='eSign', initial=INIT_STATE_NAME)
e_sign_statechart.add_state(state=root_state, parent=None)
init_hibernation_state(root_state)
