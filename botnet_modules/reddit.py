import random
from botnet.modules import BaseResponder
from . import MemoryCache, get_url


def get_subreddit_listing(name):
    url = 'https://www.reddit.com/r/%s/hot.json' % name
    return get_url(url).json()


class Reddit(BaseResponder):
    """Performs reddit-related actions."""

    def __init__(self, config):
        super(Reddit, self).__init__(config)
        self.c = MemoryCache(120)

    def _get_random_post(self, subreddit):
        """Returns a random hot post from a subreddit."""
        v = self.c.get(subreddit)
        if v is None:
            v = get_subreddit_listing(subreddit)
            self.c.set(subreddit, v)
        return random.choice(v['data']['children'])

    def command_blazeit(self, msg):
        """Grabs a random hot link from /r/montageparodies."""
        attempts = 0
        while attempts < 10:
            v = self._get_random_post('montageparodies')
            if not v['data']['is_self']:
                self.respond(msg, 'Here is your meme: %s' % v['data']['url'])
                break
            attempts += 1


mod = Reddit
