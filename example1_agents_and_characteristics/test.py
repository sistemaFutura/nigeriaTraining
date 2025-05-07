import unittest
import random
from runner import Person, DigitalServicesModel  # Cambia 'your_module_name' si el archivo se llama diferente

class TestPerson(unittest.TestCase):

    def test_initial_state_random(self):
        # Test logical: initial state should be True or False
        person = Person(0.2, 0.3)
        self.assertIn(person.using_digital_services, [True, False])

    def test_step_when_using_services(self):
        random.seed(1)  # Control randomness
        person = Person(prob_stopping_use=1.0, prob_starting_use=0.0)  # Always stop
        person.using_digital_services = True
        person.step()
        self.assertFalse(person.using_digital_services)

    def test_step_when_not_using_services(self):
        random.seed(1)
        person = Person(prob_stopping_use=0.0, prob_starting_use=1.0)  # Always start
        person.using_digital_services = False
        person.step()
        self.assertTrue(person.using_digital_services)

    def test_invalid_probabilities(self):
        with self.assertRaises(ValueError):
            # Checking invalid probability (should you want to handle that)
            _ = Person(prob_stopping_use=-0.1, prob_starting_use=1.1)

class TestDigitalServicesModel(unittest.TestCase):

    def test_model_step_changes_state(self):
        random.seed(2)
        model = DigitalServicesModel(10, 0.5, 0.5)
        states_before = [agent.using_digital_services for agent in model.agents]
        model.step()
        states_after = [agent.using_digital_services for agent in model.agents]
        # Check that at least one agent has changed state
        self.assertNotEqual(states_before, states_after)

    def test_run_multiple_steps(self):
        random.seed(3)
        model = DigitalServicesModel(10, 0.5, 0.5)
        model.run(steps=3)
        # After run, we should still have all agents
        self.assertEqual(len(model.agents), 10)

    def test_zero_agents(self):
        model = DigitalServicesModel(0, 0.5, 0.5)
        model.run(steps=3)
        # No agents to change, but should not crash
        self.assertEqual(len(model.agents), 0)

    def test_extreme_probabilities(self):
        # Always stop using
        model = DigitalServicesModel(5, 1.0, 0.0)
        for agent in model.agents:
            agent.using_digital_services = True
        model.step()
        for agent in model.agents:
            self.assertFalse(agent.using_digital_services)

        # Always start using
        model = DigitalServicesModel(5, 0.0, 1.0)
        for agent in model.agents:
            agent.using_digital_services = False
        model.step()
        for agent in model.agents:
            self.assertTrue(agent.using_digital_services)

if __name__ == "__main__":
    unittest.main()


"""
corrección

class Person:
    def __init__(self, prob_stopping_use, prob_starting_use):
        if not (0.0 <= prob_stopping_use <= 1.0):
            raise ValueError("prob_stopping_use must be between 0 and 1.")
        if not (0.0 <= prob_starting_use <= 1.0):
            raise ValueError("prob_starting_use must be between 0 and 1.")

        self.prob_stopping_use = prob_stopping_use
        self.prob_starting_use = prob_starting_use
        self.using_digital_services = random.choice([True, False])


"""