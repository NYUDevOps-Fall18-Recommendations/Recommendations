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
  	   	|  4 | iphone Case       | iPhone            | Electronics |
  		  |  5 | airpod            | iPhone            | Electronics |

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
