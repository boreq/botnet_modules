from botnet.config import Config
from botnet.signals import message_in
from botnet_modules import tell
from helpers import make_message
import pytest


class TestMessageStore(object):

    @pytest.fixture
    def ms(self, tmp_file):
        return tell.MessageStore(tmp_file)

    def test_exists(self, ms):
        msg = ('recipient', 'sender', 'text')
        assert not ms.exists(*msg)
        assert ms.add(*msg)
        assert ms.exists(*msg)

    def test_add(self, ms):
        msg = ('recipient', 'sender', 'text')
        assert ms.add(*msg)
        assert not ms.add(*msg)

    def test_get_all(self, ms):
        assert ms.add('recipient', 'sender', 'msg1')
        assert ms.add('recipient', 'sender', 'msg2')
        assert len(ms.get_all('other_recipient')) == 0
        assert len(ms.get_all('recipient')) == 2
        assert not ms.exists('recipient', 'sender', 'msg1')
        assert not ms.exists('recipient', 'sender', 'msg2')

    def test_save(self, tmp_file):
        ms1 = tell.MessageStore(tmp_file)
        assert ms1.add('recipient', 'sender', 'msg')
        ms2 = tell.MessageStore(tmp_file)
        ms2.load()
        assert ms2.exists('recipient', 'sender', 'msg')


class TestTell(object):

    @pytest.fixture
    def config(self, tmp_file):
        config = {
            'module_config': {
                'tell': {
                    'data_file': tmp_file
                },
                'base_responder': {
                    'command_prefix': '.'
                }
            }
        }
        return Config(config)

    @pytest.fixture
    def mod(self, config):
        return tell.mod(config)

    def test_tell(self, msg_t, mod):
        msg = make_message('#channel :.tell recipient something important')
        message_in.send(self, msg=msg)
        assert msg_t.msg.to_string() == 'PRIVMSG #channel :Will do, nick.'
        msg = make_message('#channel :test', prefix=':recipient!~user@example.com')
        message_in.send(self, msg=msg)
        assert msg_t.msg.to_string().endswith('something important')

    def test_tell_twice(self, msg_t, mod):
        msg = make_message('#channel :.tell recipient something')
        message_in.send(self, msg=msg)
        assert msg_t.msg.to_string() == 'PRIVMSG #channel :Will do, nick.'
        msg_t.reset()
        message_in.send(self, msg=msg)
        assert msg_t.msg is None
