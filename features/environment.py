"""
Environment setup for Behavior testing

Test cases can be run with the following:
Behave
"""
import os
from behave import *
from selenium import webdriver

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

def before_all(context):
    """ Executed once before all tests """
    context.driver = webdriver.PhantomJS()
    context.driver.set_window_size(1120, 550)
    context.base_url = BASE_URL
