from botnet.config import Config
from botnet.signals import message_in
from botnet_modules import cybot
from helpers import make_message
import pytest

@pytest.fixture
def config():
    config = {
        'module_config': {
            'base_responder': {
                'command_prefix': '.'
            }
        }
    }
    return Config(config)

@pytest.fixture
def mod(config):
    return cybot.mod(config)


def test_booty(msg_t, mod):
    msg = make_message('.booty')
    message_in.send(None, msg=msg)
    assert msg_t.msg is not None


def test_shrug(msg_t, mod):
    msg = make_message('.shrug')
    message_in.send(None, msg=msg)
    assert msg_t.msg is not None


def test_cute(msg_t, mod):
    msg = make_message('#channel :.cute')
    message_in.send(None, msg=msg)
    assert msg_t.msg is not None

    msg_t.reset()

    msg = make_message('#channel :.cute nick1')
    message_in.send(None, msg=msg)
    assert 'nick1' in msg_t.msg.to_string()

    msg_t.reset()

    msg = make_message('#channel :.cute nick1 nick2')
    message_in.send(None, msg=msg)
    assert 'nick1' in msg_t.msg.to_string() and 'nick2' in msg_t.msg.to_string()


def test_triforce(msg_t, mod):
    msg = make_message('#channel :.triforce')
    message_in.send(None, msg=msg)
    assert msg_t.msg is not None


def test_implying(msg_t, mod):
    msg = make_message('#channel :.implying')
    message_in.send(None, msg=msg)
    assert 'itself' in msg_t.msg.to_string()


def test_int1(msg_t, mod):
    msg = make_message('#channel :.int ayy')
    message_in.send(None, msg=msg)
    assert 'ayy intensifies' in msg_t.msg.to_string()


def test_int2(msg_t, mod):
    msg = make_message('#channel :.INT ayy')
    message_in.send(None, msg=msg)
    assert 'AYY INTENSIFIES' in msg_t.msg.to_string()
