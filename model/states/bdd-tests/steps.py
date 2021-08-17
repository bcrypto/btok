from sismic.bdd import map_action, map_assertion

map_action('I enter wrong pin', 'I send event pin_wrong')
map_action('I enter the correct pin', 'I send event pin_ok')
map_action('I enter the correct can', 'I send event correct_can')

map_assertion('I have {tries} more try', 'variable pin_count equals {tries}')
map_assertion('Pin still active', 'variable pin_state equals \'A\'')
map_assertion('I must input can', 'state inputCan is active')
map_assertion('I must input pin', 'state input is active')
map_assertion('I must input puk', 'state inputPuk is active')
