from sismic.io import export_to_yaml, export_to_plantuml

from passwords_statechart import statechart

export_to_yaml(statechart, 'passwordBTOK.yml')
# print(export_to_plantuml(statechart))
