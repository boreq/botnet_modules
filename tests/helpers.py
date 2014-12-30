from botnet.message import Message


def make_message(text, prefix=':nick!~user@1-2-3-4.example.com'):
    text = '%s PRIVMSG %s' % (prefix, text)
    msg = Message()
    msg.from_string(text)
    return msg
