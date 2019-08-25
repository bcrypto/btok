from sismic.io import export_to_yaml, export_to_plantuml

from statecharts.crypto_token_statechart import crypto_token_statechart
from statecharts.e_sign import e_sign_statechart
from statecharts.passwords_statechart import passwords_statechart

export_to_yaml(e_sign_statechart, 'statecharts/results/eSignStates.yml')
# print(export_to_plantuml(e_sign_statechart))
