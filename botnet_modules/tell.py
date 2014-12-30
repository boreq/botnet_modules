import datetime
import threading
from botnet.modules import BaseResponder, parse_command
from botnet.helpers import load_json, save_json
from botnet.logging import get_logger


class MessageStore(list):
    """Used for storing messages which should be passed to the users."""

    def __init__(self, file_path, *args, **kwargs):
        super(MessageStore, self).__init__(*args, **kwargs)
        self.logger = get_logger(self)
        self.file_path = file_path
        self.lock = threading.Lock()
        self._messages = {}

    def load(self):
        """Loads messages from the data file."""
        try:
            self._messages = load_json(self.file_path)
        except (FileNotFoundError, ValueError) as e:
            self.logger.warning(str(e))

    def save(self):
        """Saves messages to the data file."""
        save_json(self.file_path, self._messages)

    def add(self, recipient, sender, text):
        """Adds a message to an interal list. It is recommened to run self.save
        after doing that.
        """
        if not self.exists(recipient, sender, text):
            if not recipient in self._messages:
                self._messages[recipient] = []
            data = {
                'sender': sender,
                'text': text,
                'time': datetime.datetime.utcnow().isoformat()
            }
            self._messages[recipient].append(data)
            self.save()
            return True
        return False

    def exists(self, recipient, sender, text):
        """Checks if an identical message already exists."""
        if recipient in self._messages:
            for stored_msg in self._messages[recipient]:
                if stored_msg['sender'] == sender and stored_msg['text'] == text:
                    return True
        return False

    def get_all(self, recipient):
        rw =  self._messages.pop(recipient, [])
        self.save()
        return rw


class Tell(BaseResponder):
    """Allows to leave messages for offline users.

    Example config:

        "tell": {
            "data_file": "/path/to/data.json"
        }

    """

    def __init__(self, config):
        super(Tell, self).__init__(config)
        self.config = config.get_for_module('tell')
        self.msg_st = MessageStore(self.config['data_file'])
        with self.msg_st.lock:
            self.msg_st.load()

    @parse_command([('recipient', 1), ('message', '+')], launch_invalid=False)
    def command_tell(self, msg, args):
        """Stores a message for a RECIPIENT and sends it when he is available.

        tell RECIPIENT MESSAGE
        """
        text = ' '.join(args.message)
        with self.msg_st.lock:
            added = self.msg_st.add(args.recipient[0], msg.nickname, text)
        if added:
            self.respond(msg, 'Will do, %s.' % msg.nickname)

    def handle_message(self, msg):
        """When a user writes a message in a channel send him all stored
        messages.
        """
        with self.msg_st.lock:
            messages = self.msg_st.get_all(msg.nickname)
        for m in messages:
            text = '%s: <%s> %s' % (msg.nickname, m['sender'], m['text'])
            self.respond(msg, text)


mod = Tell
