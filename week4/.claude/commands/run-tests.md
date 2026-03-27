# Intent
Run backend tests using pytest and provide a summary of the results, specifically highlighting any failures and suggesting fixes.

# Inputs
- `test_path` (optional): The specific test file or directory to run. Defaults to `backend/tests/`.

# Output
A summary of the test execution, detailing passed/failed tests, and next steps if there are failures.

# Steps
1. Run the command: `pytest {test_path:-backend/tests/} -v`
2. Parse the output to identify any failing tests.
3. If there are failures, output a brief explanation of why the test might have failed based on the error message.
4. If all tests pass, output: "✅ All tests passed successfully. Safe to proceed."