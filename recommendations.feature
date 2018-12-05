Feature: The recommendations service back-end
  As a e-commerce seller
  I need a RESTful catalog of recommendations
  So that I can keep track of recommendations

Background:
    Given the following pets
        | id | productuid        | suggestionid | categoryid  |
        |  1 | Infinity Gauntlet | Soul Stone   | Comics      |
        |  2 | iPhone            | iphone Case  | Electronics |
  
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
