#By Saiful Salim. 28/05/19.
#This unittest is mostly referred from https://github.com/jwblin/ab_cattle
#repo, CSS458 May22 Panopto Recording, 
#and https://docs.python.org/3/library/unittest.html

""" Unittest for the WaterDynamics package

    To execute, do python test.py from tests directory
    
    This is the test runner to run all the modules
    listed in the package directory

"""

#Check to see if we're running as the main method.
#If we are, we will put the parent directory to the python path
#where python searches for packages in order to import

#use >>import sys >>sys.path  to see the python path

import os
if (__name__ == '__main__') and (__package__ is None):
    filename = os.path.abspath(__file__)
    tests_dir = os.path.dirname(filename)
    package_dir = os.path.dirname(tests_dir)
    parent_to_package_dir = os.path.dirname(package_dir)
    os.sys.path.append(parent_to_package_dir)

    
    
#import statements
import copy
import unittest
#from WaterDynamics import displaying_fluid
import test_displaying_fluid


#Set up the class for all the tests
class SetUpTest(unittest.TestCase):
    """ Common data for all the tests in the the package
        Make sure capitalization is correct
    """
    def setUp(self):
        self.string_test = "Water cool"
  

#The example tests
class Tests(object):
    """ Tests of the SetUpTest class
    """
    def test_SetUpTest_string_test(self):
        self.assertTrue(self.string_test == "Water cool")
    
        #some example tests from docs.python.org/3/library/unittest.html    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())



#The actual Test Class
#These are classes that will be added to the TestSuite. The class
#
class SetUpTests( SetUpTest, Tests): pass
class DisplayFluidTests( SetUpTest, test_displaying_fluid.Tests ): pass


#Main Program
if __name__ == "__main__":
    run_verbose = True
    run_verbose = False
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SetUpTests))
    suite.addTest(unittest.makeSuite(DisplayFluidTests))
    
    
    if run_verbose:    
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        unittest.TextTestRunner(verbosity=1).run(suite)

#eof