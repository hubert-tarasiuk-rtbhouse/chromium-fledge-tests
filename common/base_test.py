# Copyright 2021 RTBHOUSE. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import sys
import logging
import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.config import config

logger = logging.getLogger(__file__)


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        # https://peter.sh/experiments/chromium-command-line-switches
        options = webdriver.ChromeOptions()
        if os.path.isfile('/home/usertd/chromium-custom/chrome'):
            logger.info("using custom chromium build")
            options.binary_location = '/home/usertd/chromium-custom/chrome'
        else:
            logger.info("using official chrome build")
            options.binary_location = '/home/usertd/chrome-linux/chrome'
        # FIXME headless chrome does not work with fledge, https://bugs.chromium.org/p/chromium/issues/detail?id=1229652
        # options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--no-zygote')
        # FIXME headless chrome does not work with fledge, https://bugs.chromium.org/p/chromium/issues/detail?id=1229652
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--user-data-dir=/tmp/profile123')
        options.add_argument('--user-agent=rtbfledgetests')
        options.add_argument('--enable-features=FledgeInterestGroups,FledgeInterestGroupAPI')
        driver = webdriver.Chrome('/home/usertd/chromedriver_linux64/chromedriver', options=options,
                                  service_args=['--enable-chrome-logs'],
                                  service_log_path=config.get('service_log_path'))
        self.driver = driver

    def tearDown(self) -> None:
        self.driver.quit()

    def assertDriverContainsText(self, css_selector, text, timeout=5):
        exc_msg = f'Failed to find text "{text}" in element "{css_selector}" '\
                  f'in given time {timeout} seconds.'
        WebDriverWait(self.driver, timeout)\
            .until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_selector), text), exc_msg)
