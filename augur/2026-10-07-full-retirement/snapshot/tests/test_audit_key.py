"""
The audit key: where it comes from, what production refuses, what warns.

The key is read once, when ``augur.kernel`` is imported, so each case runs in a
fresh interpreter with a controlled environment. Nothing here touches the real
audit log: cases that append use a log file in a temporary directory.

Run with:  python -m unittest discover -s tests -v
"""

import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLISHED_DEFAULT = "development-key"
REFUSAL = "Production deployments require unique cryptographic keys"
UNSET_WARNING = "AUGUR_AUDIT_KEY is not set"
PUBLISHED_WARNING = "published development key"
PRINT_KEY = "import augur.kernel as k; print(k._AUDIT_KEY)"


def run_kernel(code=PRINT_KEY, **env_overrides):
    """Run ``code`` in a fresh interpreter. A value of None removes that variable."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("AUGUR_")}
    for name, value in env_overrides.items():
        if value is None:
            env.pop(name, None)
        else:
            env[name] = value
    return subprocess.run(
        [sys.executable, "-W", "default", "-c", code],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=120,
    )


def signed_record(log_path):
    """The last audit line, split into its record and its signature."""
    with open(log_path) as handle:
        record = json.loads(handle.read().splitlines()[-1])
    signature = record.pop("hmac")
    body = json.dumps(record, separators=(",", ":"), sort_keys=True).encode()
    return signature, body


class TestKeySource(unittest.TestCase):
    def test_unset_outside_production_uses_a_random_key_and_warns(self):
        result = run_kernel()
        self.assertEqual(result.returncode, 0, result.stderr)
        key = result.stdout.strip()
        self.assertRegex(key, r"^[0-9a-f]{64}$")
        self.assertNotEqual(key, PUBLISHED_DEFAULT)
        self.assertIn("RuntimeWarning", result.stderr)
        self.assertIn(UNSET_WARNING, result.stderr)

    def test_the_random_key_differs_between_processes(self):
        self.assertNotEqual(run_kernel().stdout.strip(), run_kernel().stdout.strip())

    def test_empty_key_is_treated_as_unset(self):
        refused = run_kernel(AUGUR_ENV="production", AUGUR_AUDIT_KEY="")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn(REFUSAL, refused.stderr)
        outside = run_kernel(AUGUR_AUDIT_KEY="")
        self.assertEqual(outside.returncode, 0, outside.stderr)
        self.assertRegex(outside.stdout.strip(), r"^[0-9a-f]{64}$")
        self.assertIn(UNSET_WARNING, outside.stderr)

    def test_a_real_key_is_used_without_any_warning(self):
        for environment in ({"AUGUR_ENV": "production"}, {}):
            with self.subTest(environment=environment):
                result = run_kernel(AUGUR_AUDIT_KEY="a-unique-secret", **environment)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "a-unique-secret")
                self.assertEqual(result.stderr, "")


class TestProductionGate(unittest.TestCase):
    def test_unset_in_production_is_refused(self):
        result = run_kernel(AUGUR_ENV="production")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RuntimeError", result.stderr)
        self.assertIn(REFUSAL, result.stderr)

    def test_the_published_default_is_refused_in_production_even_when_set_explicitly(self):
        result = run_kernel(AUGUR_ENV="production", AUGUR_AUDIT_KEY=PUBLISHED_DEFAULT)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RuntimeError", result.stderr)
        self.assertIn(REFUSAL, result.stderr)

    def test_the_published_default_outside_production_is_used_but_warns(self):
        result = run_kernel(AUGUR_AUDIT_KEY=PUBLISHED_DEFAULT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), PUBLISHED_DEFAULT)
        self.assertIn("RuntimeWarning", result.stderr)
        self.assertIn(PUBLISHED_WARNING, result.stderr)

    def test_only_exactly_production_is_gated(self):
        """Another environment name with no key is allowed, with the unset-key warning."""
        for name in ("development", "staging", "test"):
            with self.subTest(environment=name):
                result = run_kernel(AUGUR_ENV=name)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertRegex(result.stdout.strip(), r"^[0-9a-f]{64}$")
                self.assertIn(UNSET_WARNING, result.stderr)


class TestSigning(unittest.TestCase):
    APPEND = "import augur.kernel as k; k.audit_append('probe', {'n': 1}); print(k._AUDIT_KEY)"

    def run_and_read(self, **env):
        with tempfile.TemporaryDirectory() as folder:
            log = os.path.join(folder, "audit.log")
            result = run_kernel(self.APPEND, AUGUR_AUDIT_LOG=log, **env)
            self.assertEqual(result.returncode, 0, result.stderr)
            signature, body = signed_record(log)
        return result.stdout.strip(), signature, body

    def test_the_configured_key_is_the_one_that_signs_the_log(self):
        _, signature, body = self.run_and_read(AUGUR_AUDIT_KEY="a-unique-secret")
        expected = hmac.new(b"a-unique-secret", body, hashlib.sha256).hexdigest()
        self.assertTrue(hmac.compare_digest(signature, expected))
        wrong = hmac.new(PUBLISHED_DEFAULT.encode(), body, hashlib.sha256).hexdigest()
        self.assertFalse(hmac.compare_digest(signature, wrong))

    def test_without_a_key_the_log_is_signed_with_the_process_key(self):
        key, signature, body = self.run_and_read()
        self.assertRegex(key, r"^[0-9a-f]{64}$")
        expected = hmac.new(key.encode(), body, hashlib.sha256).hexdigest()
        self.assertTrue(hmac.compare_digest(signature, expected))

    def test_without_a_key_the_log_does_not_verify_under_the_published_default(self):
        _, signature, body = self.run_and_read()
        forged = hmac.new(PUBLISHED_DEFAULT.encode(), body, hashlib.sha256).hexdigest()
        self.assertFalse(hmac.compare_digest(signature, forged))


if __name__ == "__main__":
    unittest.main()
