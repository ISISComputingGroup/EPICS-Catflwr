import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc

DEVICE_PREFIX = "CATFLWR_01"

IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("CATFLWR"),
        "macros": {},
        "emulator": "Catflwr",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class CatflwrTests(unittest.TestCase):
    """
    Tests for the Catflwr IOC.
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Catflwr", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_timeout=30)

    @parameterized.expand([[2, 3, 0], [1, 2, 1], [4, 4, 2]])
    def test_GIVEN_expected_defaults_from_device_WHEN_getting_getting_each_pv_THEN_defaults_match_pv_values(
        self, state_num, block_num, take_data
    ):
        self._lewis.backdoor_set_on_device("state_num", state_num)
        self._lewis.backdoor_set_on_device("block_num", block_num)
        self._lewis.backdoor_set_on_device("take_data", take_data)

        self.ca.assert_that_pv_is("STATE_NUM", state_num)
        self.ca.assert_that_pv_is("BLOCK_NUM", block_num)
        expected_take_data = (
            "Don't acquire" if take_data == 0 else "Acquire" if take_data == 1 else "Stop acquiring"
        )
        self.ca.assert_that_pv_is("TAKE_DATA", expected_take_data)
