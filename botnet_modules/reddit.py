import random
from botnet.modules import BaseResponder
from .lib.cache import MemoryCache
from .lib.helpers import get_url


_subreddit_hot_url = 'https://www.reddit.com/r/%s/hot.json' 


def get_subreddit_listing(name):
    url = _subreddit_hot_url % name
    return get_url(url).json()


class Reddit(BaseResponder):
    """Performs reddit-related actions."""

    def __init__(self, config):
        super(Reddit, self).__init__(config)
        self.cache = MemoryCache(300)

    def _get_random_post(self, subreddit):
        """Returns a random hot post from a subreddit."""
        key = 'hot_%s' % subreddit
        v = self.cache.get(key)
        if v is None:
            v = get_subreddit_listing(subreddit)
            self.cache.set(key, v)
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
