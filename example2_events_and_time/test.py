import unittest
import pandas as pd
from io import StringIO
from model import DigitalInclusionModel


class TestLogicalChecks(unittest.TestCase):
    def setUp(self):
        self.test_data = StringIO("""ID,Education Level,Digital Literacy Level,Uses Digital Services,Stopping Probability
1,Bachelor's,6,False,0.1
2,High School,4,False,0.2
""")
        self.df = pd.read_csv(self.test_data)
        self.df.to_csv("test_data.csv", index=False)

    def test_organization_promotes_correctly(self):
        model = DigitalInclusionModel("test_data.csv", campaign_capacity=2, campaign_effectiveness=1.5)
        model.bank.campaign_capacity = 2
        model.step()
        promoted = sum(p.using_digital_services for p in model.people)
        self.assertEqual(promoted, 1)  # Solo la persona con literacy >= 5 debe ser promovida


class TestBoundaryPolicyIncrement(unittest.TestCase):
    def setUp(self):
        self.test_data = StringIO("""ID,Education Level,Digital Literacy Level,Uses Digital Services,Stopping Probability
1,Bachelor's,9.8,False,0.1
2,High School,10,False,0.1
3,Master's,0,False,0.1
""")
        df = pd.read_csv(self.test_data)
        df.to_csv("test_data.csv", index=False)

    def test_policy_digital_literacy_bounds(self):
        model = DigitalInclusionModel("test_data.csv", campaign_capacity=0, campaign_effectiveness=1.1)
        model.step()
        values = [p.digital_literacy_level for p in model.people]
        self.assertEqual(values[0], 10)  # 9.8 * 1.1 = 10 (limitado)
        self.assertEqual(values[1], 10)  # Ya está en 10, se mantiene
        self.assertEqual(values[2], 0.5)  # Era 0, debe incrementarse


class TestErrorHandling(unittest.TestCase):
    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            DigitalInclusionModel("nonexistent.csv", 1, 5)

    def test_unknown_education_level_is_handled(self):
        test_data = StringIO("""ID,Education Level,Digital Literacy Level,Uses Digital Services,Stopping Probability
1,Unknown,6,False,0.1
""")
        df = pd.read_csv(test_data)
        df.to_csv("test_data.csv", index=False)

        model = DigitalInclusionModel("test_data.csv", campaign_capacity=1, campaign_effectiveness=1.0)
        model.bank.step()
        model.step()
        self.assertTrue(model.people[0].using_digital_services)


class TestDataRepresentation(unittest.TestCase):
    def setUp(self):
        self.test_data = StringIO("""ID,Education Level,Digital Literacy Level,Uses Digital Services,Stopping Probability
1,Bachelor's,4.5,False,0.1
""")
        self.df = pd.read_csv(self.test_data)
        self.df.to_csv("test_data.csv", index=False)

    def test_policy_agent_increases_literacy(self):
        model = DigitalInclusionModel("test_data.csv", 0, 0)
        person = model.people[0]
        self.assertEqual(person.digital_literacy_level, 4.5)
        model.step()
        self.assertEqual(person.digital_literacy_level, 5.0)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_data = StringIO("""ID,Education Level,Digital Literacy Level,Uses Digital Services,Stopping Probability
1,Bachelor's,4,False,0.1
2,Bachelor's,5,False,0.1
3,High School,3,False,0.1
""")
        self.df = pd.read_csv(self.test_data)
        self.df.to_csv("test_data.csv", index=False)

    def test_model_runs_complete_cycle(self):
        model = DigitalInclusionModel("test_data.csv", campaign_capacity=2, campaign_effectiveness=1.2)
        for _ in range(5):
            model.step()
        users = sum(p.using_digital_services for p in model.people)
        self.assertGreaterEqual(users, 2)


if __name__ == "__main__":
    unittest.main()
