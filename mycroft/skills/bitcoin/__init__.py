from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
import requests


class BitcoinSkill(MycroftSkill):
    def __init__(self):
        super(BitcoinSkill, self).__init__(name="BitcoinSkill")

    def initialize(self):

        intent = IntentBuilder("BitcoinIntent").require("BitcoinKeyword").build()
        self.register_intent(intent, self.handle_intent)

    def __register_prefixed_regex(self, prefixes, suffix_regex):
        for prefix in prefixes:
            self.register_regex(prefix + ' ' + suffix_regex)

    def handle_intent(self, message):
        price = requests.get("https://api.bitcoinaverage.com/all").json()['EUR']['averages']['24h_avg']
        self.speak("The current bitcoin price is "+str(price)+" euros.")
        self.add_result("bitcoin_price", str(price))
        self.emit_results()

    def stop(self):
        pass


def create_skill():
    return BitcoinSkill()
