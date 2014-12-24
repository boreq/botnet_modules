import sys
import traceback
from botnet.modules import BaseIdleModule
from botnet.signals import on_exception


class ExceptionMonitor(BaseIdleModule):
    """Gathers data about exceptions."""

    def __init__(self, config):
        super(ExceptionMonitor, self).__init__(config)
        on_exception.connect(self.on_exception)

    def on_exception(self, sender, **kwargs):
        e = kwargs['e']
        self.logger.error(repr(e))
        self.logger.error(''.join(traceback.format_tb(e.__traceback__)))


mod = ExceptionMonitor
