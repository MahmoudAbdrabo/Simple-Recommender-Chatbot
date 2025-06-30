import json
import random

class IntentClassifier:
    def __init__(self, intents_path):
        with open(intents_path, "r", encoding="utf-8") as f:
            self.intents = json.load(f)

    def classify(self, user_input):
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                if pattern.lower() in user_input.lower():
                    return intent["tag"]
        return "unknown"

    def get_response(self, tag):
        for intent in self.intents["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
        return "I did not understand your question ."
