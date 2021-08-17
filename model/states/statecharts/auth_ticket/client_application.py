from sismic.model import Statechart, CompoundState, BasicState, Transition

from statecharts.auth_ticket.application_system import APP_SYSTEM_SEND_REQUEST
from statecharts.auth_ticket.id_service import RETURN_CERTIFICATE_FROM_ID_SERVICE

INIT_STATE_NAME = 'hibernation'
CLIENT_SEND_REQUEST = 'client_app_send_request and start_bpace'
COMMON_KEY_CA_CT_GENERATED_EVENT = 'BPACE finished'
COMMON_KEY_CA_CT = 'K0'
COMMON_KEY_CA_CT_FLAG = f"is_{COMMON_KEY_CA_CT}_generated"
COMMON_KEY_CA_CT_GENERATED = f"{COMMON_KEY_CA_CT_FLAG}=True"
COMMON_KEY_CA_CT_INIT = f"{COMMON_KEY_CA_CT_FLAG}=False"


def init_hibernation_state(root_state):
    hibernation_state = BasicState(name=INIT_STATE_NAME)
    client_application_statechart.add_state(state=hibernation_state, parent=root_state.name)
    client_application_statechart.add_transition(Transition(source=hibernation_state.name,
                                                            target=create_check_auth_request_state(root_state).name,
                                                            event=APP_SYSTEM_SEND_REQUEST))
    client_application_statechart.add_transition(Transition(source=hibernation_state.name,
                                                            target=create_bauth_key_generation_state(root_state).name,
                                                            event=RETURN_CERTIFICATE_FROM_ID_SERVICE))


def create_bauth_key_generation_state(root_state):
    bauth_key_generation = BasicState(name='Generate key with CT by BAUTH')
    client_application_statechart.add_state(state=bauth_key_generation, parent=root_state.name)


def create_check_auth_request_state(root_state):
    check_auth_request = BasicState(name='Check auth request')
    client_application_statechart.add_state(state=check_auth_request, parent=root_state.name)
    client_application_statechart.add_transition(Transition(source=check_auth_request.name,
                                                            target=create_bpace_key_generation_state(root_state).name,
                                                            event=CLIENT_SEND_REQUEST))


def create_bpace_key_generation_state(root_state):
    bpace_key_generation = BasicState(name='Generate key with CT by BPACE',
                                      on_entry=COMMON_KEY_CA_CT_INIT,
                                      on_exit=COMMON_KEY_CA_CT_GENERATED)
    client_application_statechart.add_state(state=bpace_key_generation, parent=root_state.name)
    client_application_statechart.add_transition(Transition(source=bpace_key_generation.name,
                                                            target=INIT_STATE_NAME,
                                                            event=COMMON_KEY_CA_CT_GENERATED_EVENT))


client_application_statechart = Statechart(name='Authentication ticket generation: Client application')
root_state = CompoundState(name='Client application', initial=INIT_STATE_NAME)
client_application_statechart.add_state(state=root_state, parent=None)
init_hibernation_state(root_state)
