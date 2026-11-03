import unittest
from kb_loader import load_rules
from engine import ForwardChainingEngine


class TestLaptopAdvisor(unittest.TestCase):
    def setUp(self):
        self.rules = load_rules("kb/laptop_rules.json")

    def test_premium_ultrabook(self):
        # Input facts -> expected recommendation: premium_ultrabook
        engine = ForwardChainingEngine(self.rules)
        engine.assert_facts(["budget_high", "portable", "long_battery"])
        engine.run()
        self.assertIn("recommend:premium_ultrabook", engine.facts)
        self.assertIn("premium_ultrabook", engine.conclusions()["recommendations"])

    def test_student_budget_ultrabook_and_linux(self):
        engine = ForwardChainingEngine(self.rules)
        engine.assert_facts(["budget_low", "office_only", "portable", "pref_os_linux"])
        engine.run()
        results = engine.conclusions()
        self.assertIn("budget_ultrabook", results["recommendations"])
        self.assertIn("linux_friendly_hw", results["specs"])

    def test_gaming_tiers(self):
        # Midrange gaming
        engine_mid = ForwardChainingEngine(self.rules)
        engine_mid.assert_facts(["gaming", "budget_medium"])
        engine_mid.run()
        self.assertIn(
            "midrange_gaming_laptop", engine_mid.conclusions()["recommendations"]
        )

        # High-end gaming & AI acceleration
        engine_high = ForwardChainingEngine(self.rules)
        engine_high.assert_facts(["gaming", "budget_high", "needs_ai_accel"])
        engine_high.run()
        results_high = engine_high.conclusions()
        self.assertIn("high_end_gaming_laptop", results_high["recommendations"])
        self.assertIn("gpu_with_tensor_cores", results_high["specs"])

    def test_creative_and_travel_specs(self):
        # Creative work, portable, large screen, travel, long battery, & macos
        engine = ForwardChainingEngine(self.rules)
        engine.assert_facts(
            [
                "creative_work",
                "portable",
                "large_screen",
                "travel_often",
                "long_battery",
                "pref_os_macos",
            ]
        )
        engine.run()
        specs = engine.conclusions()["specs"]
        self.assertIn("ram_16_plus", specs)
        self.assertIn("display_15_plus_color_accurate", specs)
        self.assertIn("battery_60wh_plus", specs)
        self.assertIn("macos_required", specs)

    def test_no_matching_rules(self):
        engine = ForwardChainingEngine(self.rules)
        engine.assert_facts(["budget_low", "gaming"])
        engine.run()
        results = engine.conclusions()
        self.assertEqual(results["recommendations"], [])
        self.assertEqual(results["specs"], [])
        self.assertEqual(len(engine.trace), 0)


if __name__ == "__main__":
    unittest.main()
