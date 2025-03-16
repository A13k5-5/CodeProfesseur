import unittest
from flask_test_api import FlaskTestApi

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(FlaskTestApi)
    
    # Run the tests
    unittest.TextTestRunner(verbosity=2).run(suite)