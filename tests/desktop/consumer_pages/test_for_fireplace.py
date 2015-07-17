#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from tests.base_test import BaseTest
from pages.desktop.consumer_pages.home import Home


class TestForFireplaceTests(BaseTest):

    @pytest.mark.nondestructive
    def test_check_api_url(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        print '*** api_url is: %s **' % mozwebqa.selenium.execute_script("return require('core/settings').api_url;")
        assert False
