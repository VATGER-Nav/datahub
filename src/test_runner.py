import unittest
import os
import sys


def run_tests():
    """
    This function runs all unit tests inside of the tests/ directory and its subdirectories.
    """

    # Get the absolute path of the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the tests/ directory next to this script
    tests_dir = os.path.join(script_dir, "tests")

    # Discover and run tests in the tests/ directory and its subdirectories
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        start_dir=tests_dir, pattern="test_*.py", top_level_dir=script_dir
    )
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    # Explicitly exit with status code based on test result
    if not result.wasSuccessful():
        sys.exit(1)  # Exit with non-zero status code if tests failed


if __name__ == "__main__":
    run_tests()
