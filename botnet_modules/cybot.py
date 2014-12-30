import random
import requests
from botnet.modules import BaseResponder, parse_command


class Cybot(BaseResponder):
    """Copies Cybot's functionality. (IT IS BETTER, YOU DON'T UNDERSTAND!!1)
    https://github.com/lovelaced/cybot
    """

    def __init__(self, config):
        super(Cybot, self).__init__(config)

    def command_booty(self, msg):
        self.respond(msg, '( ͡° ͜ʖ ͡°)')

    def command_shrug(self, msg):
        self.respond(msg, '¯\_(ツ)_/¯')

    @parse_command([('nicks', '*')])
    def command_cute(self, msg, args):
        nicks = ' '.join(args.nicks)
        text = '(✿◠‿◠)っ~ ♥ {}'.format(nicks)
        self.respond(msg, text)

    def command_implying(self, msg):
        text = ('>implying is used in a mocking manner to challenge an '
        '"implication" that has been made, or sometimes it can be simply used '
        'as a joke in itself.')
        self.respond(msg, text)

    def command_memearrows(self, msg):
        text = 'Meme arrows are often used to preface implications or feels.'
        self.respond(msg, text)

    def command_triforce(self, msg):
        for text in  ['▲', '▲ ▲']:
            n = random.randint(1, 3)
            self.respond(msg, ' ' * n + text)

    @parse_command([('text', '+')], launch_invalid=False)
    def command_tweet(self, msg, args):
        data = {'tweet': ' '.join(args.text)}
        r = requests.post('http://carta.im/tweetproxy/', data=data)
        if '200' in r.text: # Disgusting, HTTP status code is always 200
            self.respond(msg, 'https://twitter.com/proxytwt')
        else:
            self.respond(msg, ':( pls fix me ;-;')

    def _get_int(self, args):
        text = ' '.join(args)
        return '[{} intensifies]'.format(text)

    @parse_command([('text', '+')], launch_invalid=False)
    def command_int(self, msg, args):
        text = self._get_int(args.text)
        self.respond(msg, text)

    @parse_command([('text', '+')], launch_invalid=False)
    def command_INT(self, msg, args):
        text = self._get_int(args.text).upper()
        self.respond(msg, text)


mod = Cybot
