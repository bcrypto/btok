from sismic.model import Statechart, CompoundState, BasicState, Transition, FinalState

TERMINAL_CT_VARIABLE = 'Ter_to_T'
CA_CT_VARIABLE = 'A_to_T'
CONNECTION_CLOSE_STATE = "'close'"
CONNECTION_ACTIVE_STATE = "'active'"
CLOSE_TERMINAL_CT_CONNECTION = f"{TERMINAL_CT_VARIABLE}={CONNECTION_CLOSE_STATE}"
CLOSE_CA_CT_CONNECTION = f"{CA_CT_VARIABLE}={CONNECTION_CLOSE_STATE}"
START_CA_CT_CONNECTION = f"{CA_CT_VARIABLE}={CONNECTION_ACTIVE_STATE}"
START_TERMINAL_CT_CONNECTION = f"{TERMINAL_CT_VARIABLE}={CONNECTION_ACTIVE_STATE}"
INIT_STATE_NAME = 'IS'
BPACE_SUCCEEDED_EVENT = "bpace_succeeded"
BAUTH_SUCCEEDED_EVENT = "bauth_succeeded"
FORCE_CONNECTION_CLOSE_EVENT = "force_connection_close"


def init_IS_state(root_state):
    crypto_token_state = BasicState(name=INIT_STATE_NAME)
    crypto_token_statechart.add_state(state=crypto_token_state, parent=root_state.name)
    crypto_token_statechart.add_transition(Transition(source=crypto_token_state.name,
                                                      target=create_PS_state(root_state).name,
                                                      event=BPACE_SUCCEEDED_EVENT))
    return crypto_token_state


def create_PS_state(parent_state):
    PS_state = BasicState(name='PS',
                          on_entry=f"{CLOSE_CA_CT_CONNECTION};{START_CA_CT_CONNECTION};{CLOSE_TERMINAL_CT_CONNECTION}")
    crypto_token_statechart.add_state(state=PS_state, parent=parent_state.name)
    crypto_token_statechart.add_transition(Transition(source=PS_state.name,
                                                      target=INIT_STATE_NAME,
                                                      event=f"{FORCE_CONNECTION_CLOSE_EVENT}:{CA_CT_VARIABLE}",
                                                      action=CLOSE_CA_CT_CONNECTION))
    crypto_token_statechart.add_transition(Transition(source=PS_state.name,
                                                      target=create_AS_state(parent_state, PS_state).name,
                                                      event=BAUTH_SUCCEEDED_EVENT))
    return PS_state


def create_AS_state(parent_state, came_from_state):
    AS_state = BasicState(name='AS', on_entry=START_TERMINAL_CT_CONNECTION)
    crypto_token_statechart.add_state(state=AS_state, parent=parent_state.name)
    crypto_token_statechart.add_transition(Transition(source=AS_state.name,
                                                      target=came_from_state.name,
                                                      event=f"{FORCE_CONNECTION_CLOSE_EVENT}:{TERMINAL_CT_VARIABLE}",
                                                      action=CLOSE_TERMINAL_CT_CONNECTION))
    crypto_token_statechart.add_transition(Transition(source=AS_state.name,
                                                      target=INIT_STATE_NAME,
                                                      event=f"{FORCE_CONNECTION_CLOSE_EVENT}:{CA_CT_VARIABLE}",
                                                      action=CLOSE_CA_CT_CONNECTION))
    crypto_token_statechart.add_transition(Transition(source=AS_state.name,
                                                      target=create_final_state(parent_state).name,
                                                      event="finish"))
    return AS_state


def create_final_state(parent_state):
    final_state = FinalState(name='final', on_entry=f"{CLOSE_CA_CT_CONNECTION};{CLOSE_TERMINAL_CT_CONNECTION}")
    crypto_token_statechart.add_state(state=final_state, parent=parent_state.name)
    return final_state


crypto_token_statechart = Statechart(name='Crypto Token states', preamble=CLOSE_TERMINAL_CT_CONNECTION)
root_state = CompoundState(name='crypto_token', initial=INIT_STATE_NAME)
crypto_token_statechart.add_state(state=root_state, parent=None)
init_IS_state(root_state)
