Feature: The recommendations service back-end
  As a e-commerce seller
  I need a RESTful catalog of recommendations
  So that I can keep track of recommendations

Background:
	Given the following recommendations
        | id | productId         | suggestionId       | categoryId  |
        |  1 | Infinity Gauntlet | Soul Stone        | Comics      |
        |  2 | iPhone            | iphone Case       | Electronics |
        |  3 | Soul Stone        | Infinity Gauntlet | Comics      |


Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Recommendation RESTful Service" in the title
  And I should not see "404 Not Found"

Scenario: Create a recommendation
  When I visit the "Home Page"
  And I set the "id" to "6"
  And I set the "productId" to "Play Station"
  And I set the "suggestionId" to "Fifa"
  And I set the "categoryId" to "Video Games"
  And I press the "Create" button
  Then I should see the message "Success"


Scenario: Update a Recommendation
    When I visit the "Home Page"
    And I set the "id" to "2"
    And I press the "Retrieve" button
    Then I should see "iPhone" in the "productId" field
    When I change "productId" to "Samsung"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "id" to "2"
    And I press the "Retrieve" button
    Then I should see "Samsung" in the "productId" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Samsung" in the results
    Then I should not see "iPhone" in the results

Scenario: Delete a Recommendation
    When I visit the "Home Page"
    And I set the "id" to "2"
    And I press the "Delete" button
    And I press the "Search" button
    Then I should not see "iPhone" in the results

Scenario: list all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "1" in the results
    And I should see "2" in the results
    And I should see "Soul Stone" in the results
