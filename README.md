# Recommendations

## Travis CI
[![Build Status](https://travis-ci.org/NYUDevOps-Fall18-Recommendations/recommendations.svg?branch=master)](https://travis-ci.org/NYUDevOps-Fall18-Recommendations/recommendations)

This is the working repository for NYU DevOps Fall 18 "Recommendations" team.


**Steps to run and test the app:** 
* clone the repository
* run command "vagrant up"
* run command "vagrant ssh"
* run command "cd /vagrant"
* run command "nosetests"


## RESTful API

### 1. List all recommendations

  GET /recommendations
  
### 2. Retrieve a single recommendation with input "id" (int)

  GET /recommendations/<id> 
  
### 3. Create a recommendation
 
  POST /recommendations
 
### 4. Delete a recommendation with input "id" (int)

  DELETE /recommendations/<id>
  
### 5. Update a recommendation with input "id" (int)

  PUT /recommendations/<id>


    


