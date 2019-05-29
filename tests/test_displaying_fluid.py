""" Define tests for unittest for module displaying_fluid
    
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


#The test
class Tests(object):
    def divide_by_two(self, a):
        """Tries to divide a by 2.0.
        """
        return a / 2.0

    def test_method_init(self):
        self.assertTrue( self.string_test == "Water cool")

    # def test_method_init_error(self):
    #     self.failUnlessRaises( TypeError, 
    #         self.divide_by_two, self.string_test == "Water cool" )


#eof