Feature: `osc addchannels` command


# common steps for all scenarios
Background:
   Given I set working directory to "{context.osc.temp}"
     And I execute osc with args "checkout test:factory test-pkgA"
     And I set working directory to "{context.osc.temp}/test:factory/test-pkgA"


Scenario: Run `osc addchannels`
    When I execute osc with args "addchannels"
    Then stdout is
        """
        Adding channels to package 'test:factory/test-pkgA'
        """


Scenario: Run `osc addchannels --enable-all`
    When I execute osc with args "addchannels --enable-all"
    Then stdout is
        """
        Adding channels to package 'test:factory/test-pkgA' options: enable-all
        """


Scenario: Run `osc addchannels --skip-disabled`
    When I execute osc with args "addchannels --skip-disabled"
    Then stdout is
        """
        Adding channels to package 'test:factory/test-pkgA' options: skip-disabled
        """
