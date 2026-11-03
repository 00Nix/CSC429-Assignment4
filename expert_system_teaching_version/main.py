from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def collect_initial_facts():
    facts = []
    # TODO: Ask more questions to collect facts for reasoning
    if input("Is portability important? (y/n): ").lower().startswith("y"):
        facts.append("portable")
    if input("Do you need long battery life? (y/n): ").lower().startswith("y"):
        facts.append("long_battery")
    if input("Is your budget high? (y/n): ").lower().startswith("y"):
        facts.append("budget_high")
    elif input("Is your budget medium? (y/n): ").lower().startswith("y"):
        facts.append("budget_medium")
    elif input("Is your budget low? (y/n): ").lower().startswith("y"):
        facts.append("budget_low")

    if input("Will you use it for gaming? (y/n): ").lower().startswith("y"):
        facts.append("gaming")
    if input("Will you use it for creative work? (y/n): ").lower().startswith("y"):
        facts.append("creative_work")
    if input("Will you need a large screen? (y/n): ").lower().startswith("y"):
        facts.append("large_screen")
    if input("Will you need AI acceleration? (y/n): ").lower().startswith("y"):
        facts.append("need_ai_accel")
    if input("Do you travel often? (y/n): ").lower().startswith("y"):
        facts.append("travel_often")
    if input("Will you use it for office work only? (y/n): ").lower().startswith("y"):
        facts.append("office_only")
    if input("Do you need a specific OS? (y/n): ").lower().startswith("y"):
        pref_os = input("Which OS do you prefer? (windows/linux/macos): ").lower()
        if pref_os in ("windows", "linux", "macos"):
            facts.append(f"pref_os_{pref_os}")

    return facts


def main():
    # TODO: Load rules, create engine, assert facts, and run inference
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)
    initial_facts = collect_initial_facts()
    engine.assert_facts(initial_facts)
    engine.run()
    results = engine.conclusions()

    print()
    if not results["recommendations"] and not results["specs"]:
        print(
            "No recommendations or specs could be inferred based on the provided facts."
        )
        return

    rule_Lookup = {step["consequent"]: step["rule"] for step in engine.trace}

    for rec in results["recommendations"]:
        rule_name = rule_Lookup.get(f"recommend:{rec}", "Unknown Rule")
        print(f"Recommendation: {rec}")
        print(f"Explanation: derived from rule '{rule_name}'")

    for spec in results["specs"]:
        rule_name = rule_Lookup.get(f"spec:{spec}", "Unknown Rule")
        print(f"Recommended Spec: {spec}")
        print(f"Explanation: derived from rule '{rule_name}'")


if __name__ == "__main__":
    main()
