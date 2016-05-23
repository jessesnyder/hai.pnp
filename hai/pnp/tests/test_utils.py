import unittest
from hai.pnp import pnputils

class TestUtils(unittest.TestCase):
    
    def test_camelize(self):
        """ Test converting strings to capitalized camel-case
        """
        self.assertEqual('MyTestName', pnputils.camelize('My Test Name'))
        self.assertEqual('MyTestName', pnputils.camelize('my test name'))
        self.assertEqual('MyTestName', pnputils.camelize('My Test name'))
        self.assertEqual('MyTestName', pnputils.camelize(' My Test name   '))
        self.assertEqual('MyTestName', pnputils.camelize('MY TEST NAME'))
        self.assertEqual('MyTestName', pnputils.camelize('MyTestName'))
        self.assertEqual('', pnputils.camelize(''))
    

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
