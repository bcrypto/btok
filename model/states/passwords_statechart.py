from sismic.model import Statechart, CompoundState, BasicState, Transition, FinalState

INPUT_STATE_NAME = 'input'
RESET_PIN_COUNT = "pin_count = 3"
INIT_STATE_PREAMBLE = RESET_PIN_COUNT + ";pin_state = 'A'"
PIN_STATE_IS_ACTIVE = "pin_state == 'A'"
PIN_STATE_IS_BLOCKED = "pin_state == 'B'"
ACCEPTABLE_PIN_COUNT = "pin_count > 1"
WRONG_PASSWORD_STATE = 'wrongPasswordState'


def init_input_state(root_state):
    input_state = BasicState(name=INPUT_STATE_NAME)
    statechart.add_state(state=input_state, parent=root_state.name)
    statechart.add_transition(Transition(source=input_state.name,
                                         target=create_correct_password_state(root_state).name,
                                         guard=PIN_STATE_IS_ACTIVE,
                                         event='pin_ok'))
    statechart.add_transition(Transition(source=input_state.name,
                                         target=create_blocked_pin_state(root_state).name,
                                         guard=PIN_STATE_IS_BLOCKED))
    statechart.add_transition(Transition(source=input_state.name,
                                         target=create_wrong_password_compound(root_state, input_state).name,
                                         guard=PIN_STATE_IS_ACTIVE,
                                         event='pin_wrong'))
    return input_state


def create_correct_password_state(parent_state):
    correct_password_state = FinalState(name='correctPassword', on_entry=RESET_PIN_COUNT)
    statechart.add_state(state=correct_password_state, parent=parent_state.name)
    return correct_password_state


def create_blocked_pin_state(parent_state):
    blocked_pin_state = BasicState(name='blockedPin')
    statechart.add_state(state=blocked_pin_state, parent=parent_state.name)
    return blocked_pin_state


def create_wrong_password_compound(parent_state, came_from_state):
    wrong_password_compound = CompoundState(name='wrongPasswordCompound',
                                            initial=WRONG_PASSWORD_STATE)
    statechart.add_state(state=wrong_password_compound, parent=parent_state.name)
    create_wrong_password_default(name=WRONG_PASSWORD_STATE,
                                  parent_state=wrong_password_compound,
                                  came_from_state=came_from_state)
    return wrong_password_compound


def create_wrong_password_default(name, parent_state, came_from_state):
    wrong_password_state = BasicState(name=name, on_entry='pin_count = pin_count - 1')
    statechart.add_state(state=wrong_password_state, parent=parent_state.name)
    statechart.add_transition(Transition(source=wrong_password_state.name,
                                         target=came_from_state.name,
                                         guard=ACCEPTABLE_PIN_COUNT))
    statechart.add_transition(Transition(source=wrong_password_state.name,
                                         target=create_can_input_state(parent_state, came_from_state).name,
                                         guard='pin_count == 1'))
    statechart.add_transition(Transition(source=wrong_password_state.name,
                                         target=create_puk_input_state(parent_state, came_from_state).name,
                                         guard='pin_count == 0',
                                         action='puk_count = 10'))
    return wrong_password_state


def create_can_input_state(parent_state, on_correct_input_state):
    can_input_state = BasicState(name='inputCan')
    statechart.add_state(state=can_input_state, parent=parent_state.name)
    statechart.add_transition(Transition(source=can_input_state.name, target=can_input_state.name, event='wrong_can'))
    statechart.add_transition(Transition(source=can_input_state.name,
                                         target=on_correct_input_state.name,
                                         event='correct_can'))
    return can_input_state


def create_puk_input_state(parent_state, main_input_state):
    puk_input_state = BasicState(name='inputPuk')
    statechart.add_state(state=puk_input_state, parent=parent_state.name)
    statechart.add_transition(Transition(source=puk_input_state.name,
                                         target=main_input_state.name,
                                         action=RESET_PIN_COUNT,
                                         event='correct_puk'))
    statechart.add_transition(Transition(source=puk_input_state.name,
                                         target=puk_input_state.name,
                                         action='puk_count = puk_count - 1',
                                         guard='puk_count > 0',
                                         event='wrong_puk'))
    statechart.add_transition(Transition(source=puk_input_state.name,
                                         target=main_input_state.name,
                                         action="pin_state = 'B'",
                                         guard='puk_count == 0',
                                         event='wrong_puk'))
    return puk_input_state


statechart = Statechart(name='BTOK passwords', preamble=INIT_STATE_PREAMBLE)
root_state = CompoundState(name='password', initial=INPUT_STATE_NAME)
statechart.add_state(state=root_state, parent=None)
init_input_state(root_state)
