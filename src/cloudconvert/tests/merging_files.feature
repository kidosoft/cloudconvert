Feature: Merging files
    I want merge two PDF files into one file


Scenario: Merge files
        Given I have created CloudConvert instance with API key "my key"
        And I have file "tests/tmp1.pdf"
        And I have file "tests/tmp2.pdf"
        When I run merging for list of PDF files
        Then I will get merged file
