"""
main (tests)

Main test runner for the fail-closed governor tests.

Source: test_governor_failclosed.py
Extracted verbatim from artifact_9.json (code_modules[].body) - not repaired.
"""

def main():
 print("
" + "=" * 70)
 print("FAIL-CLOSED GOVERNOR TESTS")
 print("=" * 70)
 tests = [
 test_safety_check_fails_closed_on_bad_json,
 test_safety_check_fails_closed_on_empty_content,
 test_safety_check_fails_closed_on_nonbool_safe,
 test_safety_check_fails_closed_on_transport_error,
 test_safety_check_approves_valid_safe_true,
 test_healing_bounds_fails_closed_no_fabricated_target,
 test_harness_fails_closed_when_no_governor,
 test_harness_blocks_unintelligible_governor,
 test_harness_approves_valid_safe_decision,
 test_harness_low_friction_needs_no_governance,
 ]
 results = []
 for t in tests:
 try:
 results.append(t())
 except Exception as e:
 print(f" FAILED: {e}")
 import traceback
 traceback.print_exc()
 results.append(False)
 passed = sum(1 for r in results if r)
 print("
" + "=" * 70)
 print(f"FAIL-CLOSED RESULTS: {passed}/{len(tests)} passed")
 print("=" * 70 + "
")
 return all(results)
