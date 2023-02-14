@wip
Feature: `osc version` command


    # common steps for all scenarios
    Background:
        Given I set working directory to "{context.osc.temp}"


    Scenario: Run `osc version`
        When I execute osc with args "version"
        Then the exit code is 0
        And stdout is
            """
            1.0.0~b4
            """
