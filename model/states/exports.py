from sismic.io import export_to_yaml, export_to_plantuml

from statecharts.crypto_token_statechart import crypto_token_statechart
from statecharts.passwords_statechart import passwords_statechart

export_to_yaml(crypto_token_statechart, 'statecharts/results/cryptoTokenStates.yml')
# print(export_to_plantuml(crypto_token_statechart))
