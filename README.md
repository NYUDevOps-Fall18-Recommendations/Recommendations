# Recommendations

## Travis CI
[![Build Status](https://travis-ci.org/NYUDevOps-Fall18-Recommendations/recommendations.svg?branch=master)](https://travis-ci.org/NYUDevOps-Fall18-Recommendations/recommendations)

This is the repository for NYU DevOps Fall 18 "Recommendations" team.


**Steps to run and test the app:** 
* clone the repository
* run command "vagrant up"
* run command "vagrant ssh"
* run command "cd /vagrant"
* run command "nosetests"


## RESTful API

### 1. List all Recommendations

  GET /recommendations
  
### 2. Returns a Recommendation with the id

  GET /recommendations/id
  
### 3. Create a Recommendation
 
  POST /recommendations
 
### 4. Deletes a Recommendation with the id

  DELETE /recommendations/id
  
### 5. Update a Recommendation with the id

  PUT /recommendations/id

### 6. Update the category of a Recommendation

  PUT /recommendations/category/<old category>


    


