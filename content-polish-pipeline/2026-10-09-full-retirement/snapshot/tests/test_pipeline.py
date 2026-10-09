"""
Tests for ContentPolishPipeline and filters.

Run with: python -m pytest
"""

import logging
import unittest
from unittest.mock import AsyncMock

from content_polish_pipeline.filters import (
    EmpiricalValidationFilter,
    PersonalPronounFilter,
    SpeculativeLanguageFilter,
)
from content_polish_pipeline.oscillation import OscillationDetector
from content_polish_pipeline.pipeline import ContentPolishPipeline

# The pipeline logs a warning when the default signing key is used; the
# tests below construct pipelines with the default key on purpose, so
# silence that logger rather than let it print to stderr.
logging.getLogger("content_polish_pipeline").addHandler(logging.NullHandler())
logging.getLogger("content_polish_pipeline").propagate = False


class TestPersonalPronounFilter(unittest.TestCase):
    def setUp(self):
        self.filter = PersonalPronounFilter()

    def test_no_pronouns(self):
        text = "The system improved performance."
        self.assertTrue(self.filter.passes(text))

    def test_first_person_singular(self):
        text = "I believe this works."
        self.assertFalse(self.filter.passes(text))
        self.assertIn("I", self.filter.violations(text))

    def test_first_person_plural(self):
        text = "We recommend this approach."
        self.assertFalse(self.filter.passes(text))
        self.assertIn("We", self.filter.violations(text))

    def test_possessive_pronouns(self):
        text = "My analysis shows improvement."
        self.assertFalse(self.filter.passes(text))

    def test_is_clean_is_alias_of_passes(self):
        for text in ("The system improved.", "I did this.", "We and my and us."):
            self.assertEqual(self.filter.is_clean(text), self.filter.passes(text))

    def test_violations_unique_and_sorted(self):
        text = "We we WE us us me my our"
        result = self.filter.violations(text)
        self.assertEqual(result, sorted(set(result)))
        self.assertEqual(len(result), len(set(result)))


class TestSpeculativeLanguageFilter(unittest.TestCase):
    def setUp(self):
        self.filter = SpeculativeLanguageFilter()

    def test_no_hedges(self):
        text = "The system improved by 50%."
        self.assertTrue(self.filter.passes(text))

    def test_might(self):
        text = "This might improve performance."
        self.assertFalse(self.filter.passes(text))

    def test_probably(self):
        text = "This probably works."
        self.assertFalse(self.filter.passes(text))

    def test_i_think(self):
        text = "I think this is good."
        self.assertFalse(self.filter.passes(text))

    def test_violations_sorted(self):
        text = "It probably might seem to appear likely, perhaps."
        result = self.filter.violations(text)
        self.assertEqual(result, sorted(result))


class TestEmpiricalValidationFilter(unittest.TestCase):
    def setUp(self):
        self.filter = EmpiricalValidationFilter()

    def test_no_evidence(self):
        text = "This is better."
        self.assertFalse(self.filter.passes(text))
        self.assertEqual(len(self.filter.violations(text)), 1)

    def test_percentage(self):
        text = "This improved by 50%."
        self.assertTrue(self.filter.passes(text))
        self.assertEqual(self.filter.violations(text), [])

    def test_metrics_word(self):
        text = "Metrics show improvement."
        self.assertTrue(self.filter.passes(text))

    def test_data_word(self):
        text = "Data demonstrates the effect."
        self.assertTrue(self.filter.passes(text))

    def test_is_clean_is_alias_of_passes(self):
        for text in ("This is better.", "Data shows a 50% gain."):
            self.assertEqual(self.filter.is_clean(text), self.filter.passes(text))


class TestContentPolishPipeline(unittest.IsolatedAsyncioTestCase):
    async def test_success_on_first_try(self):
        mock_llm = AsyncMock(
            return_value="The system demonstrated a 25% performance improvement."
        )

        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=3)
        result = await pipeline.execute("Summarize the results.")

        self.assertEqual(result["execution_status"], "SUCCESS")
        self.assertEqual(result["retry_attempts"], 1)
        self.assertIsNotNone(result["validated_content"])
        self.assertEqual(len(result["violations"]), 0)

    async def test_retry_on_pronouns(self):
        responses = [
            "I believe this is a good result.",
            "Analysis shows this is a good result with 30% improvement.",
        ]
        mock_llm = AsyncMock(side_effect=responses)

        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=5)
        result = await pipeline.execute("Summarize the results.")

        self.assertEqual(result["execution_status"], "SUCCESS")
        self.assertEqual(result["retry_attempts"], 2)
        self.assertIn("good result with 30% improvement", result["validated_content"])

    async def test_max_attempts_exhausted(self):
        mock_llm = AsyncMock(return_value="I think this might be good.")

        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=2)
        result = await pipeline.execute("Summarize the results.")

        self.assertEqual(result["execution_status"], "CRITICAL_FAILURE")
        self.assertEqual(result["retry_attempts"], 2)
        self.assertIsNone(result["validated_content"])
        self.assertGreater(len(result["violations"]), 0)

    async def test_gateway_error(self):
        mock_llm = AsyncMock(side_effect=RuntimeError("LLM timeout"))

        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=3)
        result = await pipeline.execute("Summarize the results.")

        self.assertEqual(result["execution_status"], "CRITICAL_FAILURE")
        self.assertIn("LLM gateway error", result["violations"][0])

    async def test_duplicate_generation_detected(self):
        # Same non-compliant output every time -> second attempt is a duplicate.
        mock_llm = AsyncMock(return_value="This is better.")

        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=4)
        result = await pipeline.execute("Summarize the results.")

        self.assertEqual(result["execution_status"], "CRITICAL_FAILURE")
        self.assertTrue(
            any("Duplicate generation detected" in v for v in result["violations"])
        )

    async def test_signature_stable_for_same_input(self):
        mock_llm = AsyncMock(return_value="Research data demonstrated a 25% gain.")
        key = b"secret-test-key"

        r1 = await ContentPolishPipeline(mock_llm, signing_key=key).execute("x")
        r2 = await ContentPolishPipeline(mock_llm, signing_key=key).execute("x")

        self.assertEqual(r1["execution_status"], "SUCCESS")
        self.assertEqual(r1["payload_signature"], r2["payload_signature"])
        self.assertEqual(len(r1["payload_signature"]), 96)  # SHA-384 hex

    def test_max_attempts_must_be_positive(self):
        mock_llm = AsyncMock(return_value="ok")
        with self.assertRaises(ValueError):
            ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=0)
        with self.assertRaises(ValueError):
            ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=-1)


class TestOscillationDetector(unittest.TestCase):
    def setUp(self):
        self.detector = OscillationDetector(max_history=32)

    def test_first_observation_returns_false(self):
        """First observation of text should return False (not yet repeated)."""
        result = self.detector.observe("Candidate accepted")
        self.assertFalse(result)

    def test_exact_repeat_returns_true(self):
        """Second identical observation should return True."""
        self.detector.observe("Candidate accepted")
        result = self.detector.observe("Candidate accepted")
        self.assertTrue(result)

    def test_normalized_repeat_with_whitespace(self):
        """Whitespace variations should normalize to same observation."""
        self.detector.observe("Candidate accepted")
        result = self.detector.observe("  candidate accepted  ")
        self.assertTrue(result)

    def test_normalized_repeat_with_case(self):
        """Case variations should normalize to same observation."""
        self.detector.observe("Candidate accepted")
        result = self.detector.observe("CANDIDATE ACCEPTED")
        self.assertTrue(result)

    def test_normalized_repeat_combined(self):
        """Combined whitespace and case variations."""
        self.detector.observe("Candidate accepted")
        result = self.detector.observe(" CANDIDATE ACCEPTED ")
        self.assertTrue(result)

    def test_distinct_outputs_return_false(self):
        """Different outputs should not trigger oscillation."""
        self.detector.observe("Candidate accepted")
        result = self.detector.observe("Candidate rejected")
        self.assertFalse(result)

    def test_reset_clears_history(self):
        """reset() should clear all history."""
        self.detector.observe("Candidate accepted")
        self.detector.reset()
        result = self.detector.observe("Candidate accepted")
        self.assertFalse(result)

    def test_bounded_history_eviction(self):
        """History should be bounded. Oldest is evicted when max_history reached."""
        small_detector = OscillationDetector(max_history=3)
        small_detector.observe("A")
        small_detector.observe("B")
        small_detector.observe("C")
        history = small_detector.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history, ["a", "b", "c"])
        # Add a fourth observation; A should be evicted
        small_detector.observe("D")
        history = small_detector.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history, ["b", "c", "d"])
        # Now A is gone; observing it again should return False (new observation)
        result = small_detector.observe("A")
        self.assertFalse(result)

    def test_history_snapshot(self):
        """get_history() should return current observations in order."""
        self.detector.observe("Alpha")
        self.detector.observe("Beta")
        self.detector.observe("Gamma")
        history = self.detector.get_history()
        self.assertEqual(history, ["alpha", "beta", "gamma"])

    def test_history_snapshot_after_reset(self):
        """get_history() should be empty after reset()."""
        self.detector.observe("Something")
        self.detector.reset()
        history = self.detector.get_history()
        self.assertEqual(history, [])

    def test_constructor_rejects_invalid_max_history(self):
        """max_history must be >= 1."""
        with self.assertRaises(ValueError):
            OscillationDetector(max_history=0)
        with self.assertRaises(ValueError):
            OscillationDetector(max_history=-1)

    def test_default_max_history_is_32(self):
        """Default max_history should be 32."""
        detector = OscillationDetector()
        # Fill history beyond 32 to verify the limit
        for i in range(35):
            detector.observe(f"Message {i}")
        history = detector.get_history()
        self.assertEqual(len(history), 32)

    def test_multiple_resets(self):
        """Detector should work correctly after multiple resets."""
        self.detector.observe("A")
        self.detector.reset()
        self.assertFalse(self.detector.observe("A"))
        self.detector.reset()
        self.assertFalse(self.detector.observe("A"))


class TestOscillationDetectorIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_oscillation_detected_signal_in_result(self):
        """Result should include oscillation_detected signal."""
        mock_llm = AsyncMock(return_value="The system improved by 25%.")
        pipeline = ContentPolishPipeline(execution_gateway=mock_llm)
        result = await pipeline.execute("Summarize results.")
        self.assertIn("oscillation_detected", result)
        self.assertIsInstance(result["oscillation_detected"], bool)

    async def test_oscillation_detected_false_on_success_no_repeat(self):
        """oscillation_detected should be False when no repeats occur."""
        mock_llm = AsyncMock(return_value="The data showed a 25% gain.")
        pipeline = ContentPolishPipeline(execution_gateway=mock_llm)
        result = await pipeline.execute("Summarize results.")
        self.assertEqual(result["execution_status"], "SUCCESS")
        self.assertFalse(result["oscillation_detected"])

    async def test_oscillation_detected_true_on_repeat(self):
        """oscillation_detected should be True when repeat is detected."""
        responses = [
            "This is better.",  # First attempt: no evidence
            "This is better.",  # Second attempt: repeat + no evidence
        ]
        mock_llm = AsyncMock(side_effect=responses)
        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=3)
        result = await pipeline.execute("Summarize results.")
        self.assertEqual(result["execution_status"], "CRITICAL_FAILURE")
        self.assertTrue(result["oscillation_detected"])

    async def test_oscillation_detected_persists_across_attempts(self):
        """oscillation_detected flag should persist once True."""
        responses = [
            "This is better.",  # Attempt 1: fails validation, no repeat
            "This is better.",  # Attempt 2: repeat detected, oscillation_detected=True
            "Data shows 50% gain.",  # Attempt 3: passes validation
        ]
        mock_llm = AsyncMock(side_effect=responses)
        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=5)
        result = await pipeline.execute("Summarize results.")
        # After detecting oscillation once, it should remain True even if validation passes
        self.assertTrue(result["oscillation_detected"])

    async def test_oscillation_isolation_between_executions(self):
        """Oscillation history should be isolated per execute() call."""
        responses_1 = [
            "This is better.",  # Fails
            "Data shows 25% gain.",  # Passes
        ]
        mock_llm_1 = AsyncMock(side_effect=responses_1)
        pipeline = ContentPolishPipeline(execution_gateway=mock_llm_1)

        result_1 = await pipeline.execute("First prompt")
        self.assertEqual(result_1["execution_status"], "SUCCESS")
        self.assertFalse(result_1["oscillation_detected"])

        # Second execution with same LLM
        responses_2 = [
            "Data shows 50% improvement.",  # Passes
        ]
        mock_llm_2 = AsyncMock(side_effect=responses_2)
        pipeline_2 = ContentPolishPipeline(execution_gateway=mock_llm_2)

        result_2 = await pipeline_2.execute("Second prompt")
        self.assertEqual(result_2["execution_status"], "SUCCESS")
        self.assertFalse(result_2["oscillation_detected"])

    async def test_oscillation_reported_in_failure(self):
        """Failure message should indicate duplicate detection."""
        mock_llm = AsyncMock(return_value="This is better.")
        pipeline = ContentPolishPipeline(execution_gateway=mock_llm, max_attempts=2)
        result = await pipeline.execute("Summarize results.")
        self.assertEqual(result["execution_status"], "CRITICAL_FAILURE")
        self.assertTrue(
            any("Duplicate generation detected" in v for v in result["violations"])
        )
