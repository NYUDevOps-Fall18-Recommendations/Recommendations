Feature: The recommendations service back-end
  As a e-commerce seller
  I need a RESTful catalog of recommendations
  So that I can keep track of recommendations

Background:
    Given the following pets
        | id | productuid        | suggestionid      | categoryid  |
        |  1 | Infinity Gauntlet | Soul Stone        | Comics      |
        |  2 | iPhone            | iphone Case       | Electronics |
        |  3 | Soul Stone        | Infinity Gauntlet | Comics      |
  		|  4 | iphone Case       | iPhone            | Electronics |
  		|  5 | airpod            | iPhone            | Electronics |
  
  
Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Recommendation RESTful Service" in the title
  And I should not see "404 Not Found"


Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "Productid" to "Grater"
    And I set the "Suggestionid" to "Cheese Grater"
    And I set the "Categoryid" to "Utensil"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Infinity Gauntlet" in the results
    And I should see "iPhone" in the results
    And I should see "Soul Stone" in the results
    And I should see "iphone Case" in the results
    And I should see "airpod" in the results

Scenario: List all Electronics
    When I visit the "Home Page"
    And I set the "Category" to "Electronics"
    And I press the "Search" button
    Then I should see "iPhone" in the results
    And I should see "iphone Case" in the results
    And I should see "airpod" in the results

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