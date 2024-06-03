from sismic.model import Statechart, BasicState, Transition, CompoundState

from statecharts.auth_ticket.client_application import CLIENT_SEND_REQUEST, COMMON_KEY_CA_CT_INIT, \
    COMMON_KEY_CA_CT_GENERATED, COMMON_KEY_CA_CT_GENERATED_EVENT
from statecharts.auth_ticket.id_service import RETURN_CERTIFICATE_FROM_ID_SERVICE

INIT_STATE_NAME = 'hibernation'


def init_hibernation_state(root_state):
    hibernation_state = BasicState(name=INIT_STATE_NAME)
    crypto_token_statechart.add_state(state=hibernation_state, parent=root_state.name)
    crypto_token_statechart.add_transition(Transition(source=hibernation_state.name,
                                                      target=create_bpace_key_generation_state(root_state).name,
                                                      event=CLIENT_SEND_REQUEST))
    crypto_token_statechart.add_transition(Transition(source=hibernation_state.name,
                                                      target=create_bauth_key_generation_state(root_state).name,
                                                      event=RETURN_CERTIFICATE_FROM_ID_SERVICE))


def create_bauth_key_generation_state(root_state):
    bauth_key_generation = BasicState(name='Generate key with CA by BAUTH')
    crypto_token_statechart.add_state(state=bauth_key_generation, parent=root_state.name)


def create_bpace_key_generation_state(root_state):
    bpace_key_generation = BasicState(name='Generate key with CA by BPACE',
                                      on_entry=COMMON_KEY_CA_CT_INIT,
                                      on_exit=COMMON_KEY_CA_CT_GENERATED)
    crypto_token_statechart.add_state(state=bpace_key_generation, parent=root_state.name)
    crypto_token_statechart.add_transition(Transition(source=bpace_key_generation.name,
                                                      target=INIT_STATE_NAME,
                                                      event=COMMON_KEY_CA_CT_GENERATED_EVENT))


crypto_token_statechart = Statechart(name='Authentication ticket generation: Crypto Token')
root_state = CompoundState(name='Crypto Token', initial=INIT_STATE_NAME)
crypto_token_statechart.add_state(state=root_state, parent=None)
init_hibernation_state(root_state)
