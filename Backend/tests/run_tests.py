import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from test_auth import test_password_hashing, test_jwt_token_encoding_and_decoding
from test_boost import test_boost_calculator_with_matches, test_boost_calculator_no_matches
from test_csv_import import test_parse_csv_english_headers, test_parse_csv_ukrainian_headers, test_parse_csv_invalid_rows
from services.scoring.ai_scorer import ProductScorer


async def run_scoring_tests():
    scorer = ProductScorer()
    scorer.api_key = ""
    scorer.llm_provider = ""

    score, reasoning = await scorer.calculate_score(
        name="Apple AirPods Pro 2",
        category="Electronics",
        rating=4.8,
        reviews=25000,
        trend_score=85.0,
        boost_score=15.0,
    )
    assert score >= 70 and score <= 99, f"Expected strong score for top product, got {score}"
    assert "Товар демонструє" in reasoning or "потенціал" in reasoning

    low_score, low_reasoning = await scorer.calculate_score(
        name="Generic Plastic Case",
        category="Other",
        rating=3.2,
        reviews=10,
        trend_score=30.0,
        boost_score=0.0,
    )
    assert low_score < 50, f"Expected low score for weak product, got {low_score}"


def main():
    print("=" * 60)
    print("  🍋 e-Commerce Score — Automated Test Suite")
    print("=" * 60)

    print("\n[1/4] Running Auth Tests (Password Hashing & JWT)...")
    test_password_hashing()
    test_jwt_token_encoding_and_decoding()
    print("  ✅ Auth tests passed.")

    print("\n[2/4] Running Sales Boost Algorithm Tests...")
    test_boost_calculator_with_matches()
    test_boost_calculator_no_matches()
    print("  ✅ Sales Boost tests passed.")

    print("\n[3/4] Running CSV Import & Aliases Tests...")
    test_parse_csv_english_headers()
    test_parse_csv_ukrainian_headers()
    test_parse_csv_invalid_rows()
    print("  ✅ CSV Import tests passed.")

    print("\n[4/4] Running Scoring & Fallback Model Tests...")
    asyncio.run(run_scoring_tests())
    print("  ✅ Scoring tests passed.")

    print("\n" + "=" * 60)
    print("  🎉 ALL UNIT & INTEGRATION TESTS PASSED (100%)")
    print("=" * 60)


if __name__ == "__main__":
    main()
