from sismic.model import Statechart, CompoundState, BasicState, Transition

from statecharts.auth_ticket.client_application import CLIENT_SEND_REQUEST

INIT_STATE_NAME = 'hibernation'
RETURN_CERTIFICATE_FROM_ID_SERVICE = 'return founded cert and cert path'


def init_hibernation_state(root_state):
    hibernation_state = BasicState(name=INIT_STATE_NAME)
    id_service_statechart.add_state(state=hibernation_state, parent=root_state.name)
    id_service_statechart.add_transition(Transition(source=hibernation_state.name,
                                                    target=create_check_received_request_state(root_state).name,
                                                    event=CLIENT_SEND_REQUEST))


def create_check_received_request_state(root_state):
    check_received_request = BasicState(name='Check Chart received from CA')
    id_service_statechart.add_state(state=check_received_request, parent=root_state.name)
    id_service_statechart.add_transition(Transition(source=check_received_request.name,
                                                    target=root_state.name,
                                                    event=RETURN_CERTIFICATE_FROM_ID_SERVICE))


id_service_statechart = Statechart(name='Authentication ticket generation: Id Service')
root_state = CompoundState(name='Id Service', initial=INIT_STATE_NAME)
id_service_statechart.add_state(state=root_state, parent=None)
init_hibernation_state(root_state)
