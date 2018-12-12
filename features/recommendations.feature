Feature: The recommendations service back-end
  As a e-commerce seller
  I need a RESTful catalog of recommendations
  So that I can keep track of recommendations

Background:
	Given the following pets
        | id | productid         | suggestionid      | categoryid  |
        |  1 | Infinity Gauntlet | Soul Stone        | Comics      |
        |  2 | iPhone            | iphone Case       | Electronics |
        |  3 | Soul Stone        | Infinity Gauntlet | Comics      |
  		  |  4 | iphone Case       | iPhone            | Electronics |
  
Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Recommendation RESTful Service" in the title
  And I should not see "404 Not Found"

Scenario: Read a recommendation
    When I visit the "Home Page"
    And I set the "Id" to "2"
    When I press the "Retrieve" button
    Then I should see "iPhone" in the "productid" field
    Then I should see "iphone Case" in the "suggestionid" field
    Then I should see "Electronics" in the "categoryid" field

Scenario: Update a Recommendation
    When I visit the "Home Page"
    And I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see "iPhone" in the "productid" field and "iphone Case" in the "suggestionid" field
    When I change "suggestionid" to "airpod"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see "airpod" in the "suggestionid" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "airpod" in the "suggestionid" field of the product "iPhone" 
    Then I should not see "iphone Case" in the "suggestionid" field of the product "iPhone"

Scenario: Delete a recommendation
    When I visit the "Home Page"
    And I set the "productid" to "iPhone"
    And I press the "Delete" button
    Then I should not see "iPhone" in the results
    When I set the "productid" to "iphone Case"
    And I press the "Retrieve" button
    Then I should see "null" in the "suggestionid" field

Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Infinity Gauntlet" in the results
    And I should see "iPhone" in the results
    And I should see "Soul Stone" in the results
    And I should see "iphone Case" in the results


