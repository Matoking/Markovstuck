from __future__ import print_function

from markovify.text import NewlineText

import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line

import os.path

import json
import random
import sys
import resource

import humanfriendly


class MarkovChain(object):
    def __init__(self):
        self.chains = {}

    def load_chains(self):
        """Load Markov chains from files"""
        from generator import settings

        chains = settings.NAMES + ["general", "title"]

        for name in chains:
            path = os.path.join(
                "chains",
                "%s.json" % name)

            if not os.path.exists(path):
                continue

            print("Loading chain %s... " % name, end="")

            f = open(path, 'r')
            data = f.read()
            f.close()

            data = json.loads(data)
            text = NewlineText.from_chain(data)

            self.chains[name] = text

            print("Loaded!")


markov_chain = MarkovChain()


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        response = {}

        generate_pre_dialog = self.get_argument(
            "generate_pre_dialog",
            default=False)

        generate_post_dialog = self.get_argument(
            "generate_post_dialog",
            default=False)

        if self.get_argument("conversation_length", default=None):
            response["dialoglog"] = []

            conversation_length = int(self.get_argument("conversation_length"))
            characters = json.loads(self.get_argument("characters"))

            for i in range(0, conversation_length):
                # Pick a random character
                character = random.choice(characters)

                entry = {"char": character,
                         "logs": []}

                for j in range(0, random.randint(1, 3)):
                    entry["logs"].append(self.generate_sentence(character))

                response["dialoglog"].append(entry)

        # Generate title
        response["title"] = self.generate_sentence("title")

        if generate_pre_dialog:
            # Generate pre-dialog text
            response["pre_dialog_text"] = self.generate_sentence("general")

        if generate_post_dialog:
            # Generate post-dialog text
            response["post_dialog_text"] = self.generate_sentence("general")

        response = json.dumps(response)

        self.write(response)

    def generate_sentence(self, name):
        """
        Generate a sentence using the provided chain
        """
        for i in range(0, 10):
            text = markov_chain.chains[name].make_sentence()

            if text is not None:
                return text

        return None


def main():
    parse_command_line()
    print("Loading markov chains...")
    markov_chain.load_chains()

    # Print memory usage for the server when all chains are loaded
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1000.0
    memory_usage = humanfriendly.format_size(memory_usage)

    print("Markov chain server loaded, memory usage %s" % memory_usage)

    application = tornado.web.Application([
        (r"/", MainHandler),
    ], debug=False)
    application.listen(5666, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
