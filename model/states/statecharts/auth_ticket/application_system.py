from sismic.model import CompoundState, Statechart, BasicState, Transition

INIT_STATE_NAME = 'hibernation'
APP_SYSTEM_SEND_REQUEST = 'app_system_send_request'


def init_hibernation_state(root_state):
    hibernation_state = BasicState(name=INIT_STATE_NAME)
    application_system_statechart.add_state(state=hibernation_state, parent=root_state.name)
    application_system_statechart.add_transition(Transition(source=hibernation_state.name,
                                                            target=create_waiting_auth_response_state(root_state).name,
                                                            event=APP_SYSTEM_SEND_REQUEST))


def create_waiting_auth_response_state(root_state):
    waiting_auth_response = BasicState(name='Waiting auth respose')
    application_system_statechart.add_state(state=waiting_auth_response, parent=root_state.name)
    #      TODO: To hibernation?


application_system_statechart = Statechart(name='Authentication ticket generation: Application system')
root_state = CompoundState(name='Application system', initial=INIT_STATE_NAME)
application_system_statechart.add_state(state=root_state, parent=None)
init_hibernation_state(root_state)
