import random
from botnet.modules import BaseResponder
from .lib.cache import MemoryCache
from .lib.helpers import get_url


_subreddit_hot_url = 'https://www.reddit.com/r/{subreddit}/{type}.json'


def get_subreddit_listing(subreddit, type='hot'):
    """Returns a subreddit listing.

    subreddit: subreddit name.
    type: one of ['hot', 'new'].
    """
    url = _subreddit_hot_url.format(subreddit=subreddit, type=type)
    return get_url(url).json()


class Reddit(BaseResponder):
    """Performs reddit-related actions."""

    def __init__(self, config):
        super(Reddit, self).__init__(config)
        self.cache = MemoryCache(300)

    def _get_hot_posts(self, subreddit):
        """Returns a listing containing hot posts from a subreddit."""
        key = 'hot_' + subreddit
        v = self.cache.get(key)
        if v is None:
            v = get_subreddit_listing(subreddit)
            self.cache.set(key, v)
        return v

    def _get_random_post(self, listing):
        """Gets a random link or text post from a listing."""
        return random.choice(listing['data']['children'])

    def _get_random_link(self, listing):
        """Gets a random link from a listing."""
        for i in range(0, 10):
            v = self._get_random_post(listing)
            if not v['data']['is_self']:
                return v['data']['url']

    def command_blazeit(self, msg):
        """Grabs a random hot link from /r/montageparodies."""
        listing = self._get_hot_posts('montageparodies')
        link = self._get_random_link(listing)
        self.respond(msg, 'Here is your meme: {}'.format(link))

    def command_aww(self, msg):
        """Grabs a random hot link from /r/cats."""
        listing = self._get_hot_posts('cats')
        link = self._get_random_link(listing)
        self.respond(msg, ':3 {}'.format(link))


mod = Reddit
