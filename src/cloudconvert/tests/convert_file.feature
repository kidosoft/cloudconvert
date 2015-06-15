Feature: File conversion
    I want to convert one file

Scenario: Convert file
        Given I have created CloudConvert instance with API key "my key"
        And I have file "tests/tmp.jpg"
        And I want convert it to "pdf"
        When I run conversion
        Then I will get converted file
