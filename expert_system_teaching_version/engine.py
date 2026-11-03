# Caleb Nix
from dataclasses import dataclass
from typing import List, Set, Dict, Any


@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""


class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Store initial facts into the working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """TODO: Return True if all antecedents are true and consequent not yet known."""
        if rule.consequent in self.facts:
            return False
        return all(antecedent in self.facts for antecedent in rule.antecedents)

    def run(self) -> None:
        """TODO: Implement the forward chaining loop."""
        # while there are rules that can fire:
        while True:
            #     select one rule (students decide tie-breaking)
            fireable_rules = [rule for rule in self.rules if self.can_fire(rule)]
            if not fireable_rules:
                break
            #     add its consequent to facts
            fireable_rules.sort(key=lambda r: r.priority, reverse=True)
            selected_rule = fireable_rules[0]
            #     record in trace
            self.facts.add(selected_rule.consequent)
            self.trace.append(
                {
                    "rule": selected_rule.name,
                    "antecedents": selected_rule.antecedents,
                    "consequent": selected_rule.consequent,
                }
            )

    def conclusions(self) -> Dict[str, List[str]]:
        """TODO: Return separated results (recommendations, specs, other facts)."""
        reccomendations = []
        specs = []
        other_facts = []

        for fact in sorted(self.facts):
            if fact.startswith("recommend:"):
                reccomendations.append(fact.split("recommend:", 1)[1])
            elif fact.startswith("spec:"):
                specs.append(fact.split("spec:", 1)[1])
            else:
                other_facts.append(fact)
        return {
            "recommendations": reccomendations,
            "specs": specs,
            "other_facts": other_facts,
        }
