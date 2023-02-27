from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply
import threading

@has_log
class CatflwrStreamInterface(StreamInterface):
    

    # Commands that we expect via serial during normal operation (No commands - the device always sends a stream of
    # information to the IOC without being polled)
    commands = {}

    in_terminator = "\r"
    out_terminator = b""

    def __init__(self):
        super(CatflwrStreamInterface, self).__init__()
        self._queue_next_unsolicited_message()

    def _queue_next_unsolicited_message(self):
        # The real device updates every 10 seconds, but as we scan with I/O Intr we can speed this up here
        timer = threading.Timer(1.0, self.get_data_unsolicited)
        timer.daemon = True
        timer.start()

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def get_data_unsolicited(self):
        self._queue_next_unsolicited_message()

        if not self.device.connected:
            return

        try:
            handler = self.handler
        except AttributeError:
            # Happens if no client is currently connected.
            return
        else:
            handler.unsolicited_reply(self._construct_status_message())

    def _construct_status_message(self):
        return f"{self.device.state_num},{self.device.block_num},{self.device.take_data}\r".encode()
