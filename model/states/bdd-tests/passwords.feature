Feature: Passwords

  Scenario: Invalid pin code 1 time and then valid
    When I enter wrong pin
    Then I have 2 more try
    When I enter the correct pin
    Then Pin still active
    Then statechart is in a final configuration

  Scenario: Invalid pin code 3 times
    When I enter wrong pin
    Then I have 2 more try
    When I enter wrong pin
    Then I have 1 more try
    Then I must input can
    When I enter the correct can
    Then I must input pin
    When I enter wrong pin
    Then I have 0 more try
    Then I must input puk
