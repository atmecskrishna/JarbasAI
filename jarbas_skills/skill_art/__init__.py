import os
from os.path import dirname
from imgurpython import ImgurClient
from mycroft.util.art import psy_art
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.messagebus.message import Message

__author__ = 'jarbas'


class ArtSkill(MycroftSkill):

    def __init__(self):
        super(ArtSkill, self).__init__(name="ArtSkill")
        self.reload_skill = False

        try:
            self.psypath = self.config_core["database_path"] + "/pictures/psy"
        except:
            self.psypath = dirname(__file__) + "/psy"

        # check if folders exist
        if not os.path.exists(self.psypath):
            os.makedirs(self.psypath)  # TODO get from config
        try:
            client_id = self.config_core.get("APIS")["ImgurKey"]
            client_secret = self.config_core.get("APIS")["ImgurSecret"]
        except:
            if self.config is not None:
                client_id = self.config.get("ImgurKey")
                client_secret = self.config.get("ImgurSecret")
            else:
                # TODO throw error
                client_id = 'xx'
                client_secret = 'yyyyyyyyy'

        try:
            self.client = ImgurClient(client_id, client_secret)
        except:
            self.client = None

    def initialize(self):
        psy_intent = IntentBuilder("PsyArtIntent").require("psyart").build()
        self.register_intent(psy_intent, self.handle_psy_pic_intent)

        self.emitter.on("art.request", self.handle_psy_pic)

    def handle_psy_pic_intent(self, message):
        self.emitter.emit(Message("art.request", {}, self.context))

    def handle_psy_pic(self, message):
        try:

            pic = psy_art(self.psypath, 1, message.data.get("name"))[0]
            link = None
            if pic is not None:
                if self.client is not None:
                    data = self.client.upload_from_path(pic)
                    link = data["link"]
                else:
                    link = None
                self.speak("Here is what i created", metadata={"url": link, "file": pic})
            self.emitter.emit(Message("art.result", {"file": pic, "url": link}, self.context))
        except Exception as e:
            self.speak(str(e))

    def stop(self):
        pass


def create_skill():
    return ArtSkill()
