import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def mod(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

class AgentRegistryTests(unittest.TestCase):
    def setUp(self):
        self.reg = json.loads((ROOT / "config/agent-registry.example.json").read_text())
        self.pol = json.loads((ROOT / "config/policy.example.json").read_text())
        self.task = json.loads((ROOT / "config/task.example.json").read_text())

    def test_initial_examples_disabled_and_valid(self):
        errors, _ = mod("doctor").validate(self.reg, self.pol)
        self.assertEqual(errors, [])
        self.assertIsNone(mod("route").choose(self.reg, self.task)["selected_agent"])

    def test_enabled_unverified_rejected(self):
        self.reg["agents"][0]["enabled"] = True
        errors, _ = mod("doctor").validate(self.reg, self.pol)
        self.assertTrue(any("without verified" in e for e in errors))

    def test_verified_candidate_can_route(self):
        agent = self.reg["agents"][0]
        agent.update({"enabled": True, "verification": "verified", "assurance_tier": 2})
        result = mod("route").choose(self.reg, self.task)
        self.assertEqual(result["selected_agent"], agent["id"])
        self.assertFalse(result["executed"])

    def test_reviewer_must_be_readonly(self):
        reviewer = self.reg["agents"][1]
        reviewer.update({"enabled": True, "verification": "verified", "assurance_tier": 2})
        errors, _ = mod("doctor").validate(self.reg, self.pol)
        self.assertTrue(any("read-only" in e for e in errors))

    def test_no_push_deploy_or_protected_merge(self):
        self.pol["allow_automatic_push"] = True
        errors, _ = mod("doctor").validate(self.reg, self.pol)
        self.assertTrue(any("push" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
