Feature: The recommendations service back-end
  As a e-commerce seller
  I need a RESTful catalog of recommendations
  So that I can keep track of recommendations
  
Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Recommendation RESTful Service" in the title
  And I should not see "404 Not Found"
