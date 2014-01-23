#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import xml.etree.cElementTree as et

jobs = {}
aggregated_results = {'Firefox OS': {}, 'Android': {}, 'Desktop': {}}
final = []
XML_FILE_ROOT_FOLDER = 'xml_results'

for file in os.listdir(XML_FILE_ROOT_FOLDER):
    if file.endswith(".xml"):
        job_name = file.split('.xml')[0]
        print file, job_name

        with open(os.path.join(XML_FILE_ROOT_FOLDER, file), 'r') as xml_file:

            tree = et.fromstring(xml_file.read())
            test_results = {}
            for el in tree.findall('testcase'):
                test = {'classname': el.attrib['classname']}
                if len(el.getchildren()) == 0:
                    test['result'] = 'passed'
                else:
                    result = el.getchildren()[0]
                    test['result'] = result.tag
                    test['detail'] = '%s: %s' % (result.attrib['message'], result.text)

                test_results[el.attrib['name']] = test

            jobs[job_name] = test_results

# print jobs

for job_name in jobs:
    if 'b2g' in job_name:
        group = 'Firefox OS'
    elif 'mobile' in job_name:
        group = 'Android'
    else:
        group = 'Desktop'
    if job_name.startswith('marketplace.dev'):
        environment = 'dev'
    elif job_name.startswith('marketplace.stage'):
        environment = 'stage'
    elif job_name.startswith('marketplace.prod'):
        environment = 'prod'
    else:
        environment = 'unknown'

    target_group = aggregated_results[group]
    for test_name in jobs[job_name]:
        test = jobs[job_name][test_name]
        if not test_name in target_group:
            target_group[test_name] = {'test_name': test_name, 'classname': test['classname'], 'passed': [], 'skipped': {}, 'failed': [], 'environments': []}
        if not environment in target_group[test_name]['environments']:
            target_group[test_name]['environments'].append(environment)
        if test['result'] == 'passed':
            target_group[test_name]['passed'].append(job_name)
        elif test['result'] == 'skipped':
            if 'jobs' in target_group[test_name]['skipped']:
                target_group[test_name]['skipped']['jobs'].append(job_name)
            else:
                target_group[test_name]['skipped'] = {'result': test['result'], 'detail': test['detail'], 'jobs': [job_name]}
        else:
            target_group[test_name]['failed'].append({'result': test['result'], 'detail': test['detail'], 'jobs': [job_name]})

for group_key in aggregated_results:
    target_group = aggregated_results[group_key]
    new_group = []
    for test_key in target_group:
        test = target_group[test_key]
        test['all_passed'] = not bool(len(test['failed']))
        new_group.append(test)
    final.append({'group': group_key, 'test_results': new_group})

# print aggregated_results
with open('final.json', 'w') as outfile:
    json.dump(final, outfile)

#
# sxml = """
# <testsuite errors="0" failures="1" name="" skips="6" tests="9" time="1223.738"><testcase classname="tests.desktop.developer_hub.test_api_submit.TestAPI" name="test_assert_that_a_app_can_be_added_by_api" time="2.43493914604"><skipped message="expected test failure">Bug 960169 - 403 response returned when trying to create an app via the Marketplace API</skipped></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_packaged_app_submission" time="241.175439119"><skipped message="expected test failure">Bug 960044 - [dev] IARC submissionID/secCode form fails + pingback never comes on -dev</skipped></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_hosted_paid_app_submission" time="244.798313141"><skipped message="xfail-marked test passes unexpectedly"/></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_hosted_app_submission" time="245.91136694"><skipped message="xfail-marked test passes unexpectedly"/></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_deletes_app" time="27.1556451321"><failure message="test failure">self = &lt;tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub instance at 0x10a062ef0&gt;
#
# mozwebqa = &lt;pytest_mozwebqa.pytest_mozwebqa.TestSetup instance at 0x10a0627e8&gt;
#
#     def test_that_deletes_app(self, mozwebqa):
#
#         dev_home = Home(mozwebqa)
#         dev_home.go_to_developers_homepage()
#         dev_home.login(user="default")
#
#         my_apps = dev_home.header.click_my_submissions()
#
#         first_free_app = my_apps.first_free_app
#         app_name = first_free_app.name
#
# &gt;       self._delete_app(mozwebqa, app_name)
#
# tests/desktop/developer_hub/test_developer_hub.py:233:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub instance at 0x10a062ef0&gt;
# mozwebqa = &lt;pytest_mozwebqa.pytest_mozwebqa.TestSetup instance at 0x10a0627e8&gt;
# app_name = u'Clastsordbenver Yleri Omcunmane'
#
#     def _delete_app(self, mozwebqa, app_name):
#         from pages.desktop.developer_hub.developer_submissions import DeveloperSubmissions
#         submitted_apps = DeveloperSubmissions(mozwebqa)
#
#         app = submitted_apps.get_app(app_name)
#
# &gt;       manage_status = app.click_manage_status_and_versions()
#
# tests/desktop/base_test.py:78:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;pages.desktop.developer_hub.developer_submissions.App object at 0x10a3bb390&gt;
#
#     def click_manage_status_and_versions(self):
# &gt;       self.find_element(*self._manage_status_and_version_locator).click()
#
# pages/desktop/developer_hub/developer_submissions.py:159:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;pages.desktop.developer_hub.developer_submissions.App object at 0x10a3bb390&gt;
# locator = ('css selector', 'a.status-link')
#
#     def find_element(self, *locator):
# &gt;       return self._selenium_root.find_element(*locator)
#
# pages/page.py:137:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;selenium.webdriver.remote.webelement.WebElement object at 0x109f8b850&gt;
# by = 'css selector', value = 'a.status-link'
#
#     def find_element(self, by=By.ID, value=None):
#         if not By.is_valid(by) or not isinstance(value, str):
#             raise InvalidSelectorException("Invalid locator values passed in")
#
#         return self._execute(Command.FIND_CHILD_ELEMENT,
# &gt;                            {"using": by, "value": value})['value']
#
# .env/lib/python2.7/site-packages/selenium/webdriver/remote/webelement.py:376:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;selenium.webdriver.remote.webelement.WebElement object at 0x109f8b850&gt;
# command = 'findChildElement'
# params = {'id': u'11', 'sessionId': u'ff9f3273772f4483a493a72f779c9da7', 'using': 'css selector', 'value': 'a.status-link'}
#
#     def _execute(self, command, params=None):
#         if not params:
#             params = {}
#         params['id'] = self._id
# &gt;       return self._parent.execute(command, params)
#
# .env/lib/python2.7/site-packages/selenium/webdriver/remote/webelement.py:369:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;selenium.webdriver.remote.webdriver.WebDriver object at 0x10a3af110&gt;
# driver_command = 'findChildElement'
# params = {'id': u'11', 'sessionId': u'ff9f3273772f4483a493a72f779c9da7', 'using': 'css selector', 'value': 'a.status-link'}
#
#     def execute(self, driver_command, params=None):
#         if not params:
#             params = {'sessionId': self.session_id}
#         elif 'sessionId' not in params:
#             params['sessionId'] = self.session_id
#
#         params = self._wrap_value(params)
#         response = self.command_executor.execute(driver_command, params)
#         if response:
# &gt;           self.error_handler.check_response(response)
#
# .env/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py:164:
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#
# self = &lt;selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x109f91b10&gt;
# response = {u'class': u'org.openqa.selenium.remote.Response', u'hCode': 1957306, u'sessionId': u'ff9f3273772f4483a493a72f779c9da7', u'state': u'no such element', ...}
#
#     def check_response(self, response):
#         status = response['status']
#         if status == ErrorCode.SUCCESS:
#             return
#         exception_class = ErrorInResponseException
#         if status == ErrorCode.NO_SUCH_ELEMENT:
#             exception_class = NoSuchElementException
#         elif status == ErrorCode.NO_SUCH_FRAME:
#             exception_class = NoSuchFrameException
#         elif status == ErrorCode.NO_SUCH_WINDOW:
#             exception_class = NoSuchWindowException
#         elif status == ErrorCode.STALE_ELEMENT_REFERENCE:
#             exception_class = StaleElementReferenceException
#         elif status == ErrorCode.ELEMENT_NOT_VISIBLE:
#             exception_class = ElementNotVisibleException
#         elif status == ErrorCode.INVALID_ELEMENT_STATE:
#             exception_class = InvalidElementStateException
#         elif status == ErrorCode.INVALID_SELECTOR \
#                 or status == ErrorCode.INVALID_XPATH_SELECTOR \
#                 or status == ErrorCode.INVALID_XPATH_SELECTOR_RETURN_TYPER:
#             exception_class = InvalidSelectorException
#         elif status == ErrorCode.ELEMENT_IS_NOT_SELECTABLE:
#             exception_class = ElementNotSelectableException
#         elif status == ErrorCode.INVALID_COOKIE_DOMAIN:
#             exception_class = WebDriverException
#         elif status == ErrorCode.UNABLE_TO_SET_COOKIE:
#             exception_class = WebDriverException
#         elif status == ErrorCode.TIMEOUT:
#             exception_class = TimeoutException
#         elif status == ErrorCode.SCRIPT_TIMEOUT:
#             exception_class = TimeoutException
#         elif status == ErrorCode.UNKNOWN_ERROR:
#             exception_class = WebDriverException
#         elif status == ErrorCode.UNEXPECTED_ALERT_OPEN:
#             exception_class = UnexpectedAlertPresentException
#         elif status == ErrorCode.NO_ALERT_OPEN:
#             exception_class = NoAlertPresentException
#         elif status == ErrorCode.IME_NOT_AVAILABLE:
#             exception_class = ImeNotAvailableException
#         elif status == ErrorCode.IME_ENGINE_ACTIVATION_FAILED:
#             exception_class = ImeActivationFailedException
#         elif status == ErrorCode.MOVE_TARGET_OUT_OF_BOUNDS:
#             exception_class = MoveTargetOutOfBoundsException
#         else:
#             exception_class = WebDriverException
#         value = response['value']
#         if isinstance(value, basestring):
#             if exception_class == ErrorInResponseException:
#                 raise exception_class(response, value)
#             raise exception_class(value)
#         message = ''
#         if 'message' in value:
#             message = value['message']
#
#         screen = None
#         if 'screen' in value:
#             screen = value['screen']
#
#         stacktrace = None
#         if 'stackTrace' in value and value['stackTrace']:
#             stacktrace = []
#             try:
#                 for frame in value['stackTrace']:
#                     line = self._value_or_default(frame, 'lineNumber', '')
#                     file = self._value_or_default(frame, 'fileName', '&lt;anonymous&gt;')
#                     if line:
#                         file = "%s:%s" % (file, line)
#                     meth = self._value_or_default(frame, 'methodName', '&lt;anonymous&gt;')
#                     if 'className' in frame:
#                         meth = "%s.%s" % (frame['className'], meth)
#                     msg = "    at %s (%s)"
#                     msg = msg % (meth, file)
#                     stacktrace.append(msg)
#             except TypeError:
#                 pass
#         if exception_class == ErrorInResponseException:
#             raise exception_class(response, message)
# &gt;       raise exception_class(message, screen, stacktrace)
# E       NoSuchElementException: Message: u'Unable to locate element: {"method":"css selector","selector":"a.status-link"}\nCommand duration or timeout: 10.01 seconds\nFor documentation on this error, please visit: http://seleniumhq.org/exceptions/no_such_element.html\nBuild info: version: \'2.35.0\', revision: \'c916b9d\', time: \'2013-08-12 15:42:01\'\nSystem info: os.name: \'Windows Server 2008 R2\', os.arch: \'x86\', os.version: \'6.1\', java.version: \'1.6.0_35\'\nSession ID: 056a9072-2671-4e9a-9c6c-fd779e11960c\nDriver info: org.openqa.selenium.firefox.FirefoxDriver\nCapabilities [{platform=XP, acceptSslCerts=true, javascriptEnabled=true, browserName=firefox, rotatable=false, locationContextEnabled=true, version=23.0.1, cssSelectorsEnabled=true, databaseEnabled=true, handlesAlerts=true, browserConnectionEnabled=true, nativeEvents=true, webStorageEnabled=true, applicationCacheEnabled=true, takesScreenshot=true}]' ; Stacktrace:
# E           at sun.reflect.NativeConstructorAccessorImpl.newInstance0 (None:-2)
# E           at sun.reflect.NativeConstructorAccessorImpl.newInstance (None:-1)
# E           at sun.reflect.DelegatingConstructorAccessorImpl.newInstance (None:-1)
# E           at java.lang.reflect.Constructor.newInstance (None:-1)
# E           at org.openqa.selenium.remote.ErrorHandler.createThrowable (ErrorHandler.java:191)
# E           at org.openqa.selenium.remote.ErrorHandler.throwIfResponseFailed (ErrorHandler.java:145)
# E           at org.openqa.selenium.remote.RemoteWebDriver.execute (RemoteWebDriver.java:554)
# E           at org.openqa.selenium.remote.RemoteWebElement.execute (RemoteWebElement.java:268)
# E           at org.openqa.selenium.remote.RemoteWebElement.findElement (RemoteWebElement.java:171)
# E           at org.openqa.selenium.remote.RemoteWebElement.findElementByCssSelector (RemoteWebElement.java:236)
# E           at org.openqa.selenium.By$ByCssSelector.findElement (By.java:407)
# E           at org.openqa.selenium.remote.RemoteWebElement.findElement (RemoteWebElement.java:167)
# E           at sun.reflect.GeneratedMethodAccessor24.invoke (None:-1)
# E           at sun.reflect.DelegatingMethodAccessorImpl.invoke (None:-1)
# E           at java.lang.reflect.Method.invoke (None:-1)
# E           at org.openqa.selenium.support.events.EventFiringWebDriver$EventFiringWebElement$1.invoke (EventFiringWebDriver.java:327)
# E           at $Proxy2.findElement (None:-1)
# E           at org.openqa.selenium.support.events.EventFiringWebDriver$EventFiringWebElement.findElement (EventFiringWebDriver.java:398)
# E           at sun.reflect.GeneratedMethodAccessor24.invoke (None:-1)
# E           at sun.reflect.DelegatingMethodAccessorImpl.invoke (None:-1)
# E           at java.lang.reflect.Method.invoke (None:-1)
# E           at org.openqa.selenium.remote.server.KnownElements$1.invoke (KnownElements.java:63)
# E           at $Proxy3.findElement (None:-1)
# E           at org.openqa.selenium.remote.server.handler.FindChildElement.call (FindChildElement.java:43)
# E           at org.openqa.selenium.remote.server.handler.FindChildElement.call (FindChildElement.java:1)
# E           at java.util.concurrent.FutureTask$Sync.innerRun (None:-1)
# E           at java.util.concurrent.FutureTask.run (None:-1)
# E           at org.openqa.selenium.remote.server.DefaultSession$1.run (DefaultSession.java:169)
# E           at java.util.concurrent.ThreadPoolExecutor$Worker.runTask (None:-1)
# E           at java.util.concurrent.ThreadPoolExecutor$Worker.run (None:-1)
# E           at java.lang.Thread.run (None:-1)
#
# .env/lib/python2.7/site-packages/selenium/webdriver/remote/errorhandler.py:164: NoSuchElementException</failure></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_editing_basic_info_for_a_free_app" time="34.9571628571"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_editing_support_information_for_a_free_app" time="24.8445489407"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_that_manifest_url_cannot_be_edited_via_basic_info_for_a_free_app" time="45.416394949"><skipped message="expected test failure">Bug 960044 - [dev] IARC submissionID/secCode form fails + pingback never comes on -dev</skipped></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_required_field_validations_on_basic_info_for_a_free_app" time="25.3257172108"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_required_field_validations_on_device_types_for_hosted_apps" time="48.192743063"><skipped message="expected test failure">Bug 960044 - [dev] IARC submissionID/secCode form fails + pingback never comes on -dev</skipped></testcase><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_a_screenshot_can_be_added" time="23.3988208771"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_a_screenshot_cannot_be_added_via_an_invalid_file_format" time="19.6936750412"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_an_icon_cannot_be_added_via_an_invalid_file_format" time="21.2711229324"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_apps_are_sorted_by_name" time="16.6909530163"/><testcase classname="tests.desktop.developer_hub.test_developer_hub.TestDeveloperHub" name="test_that_checks_apps_are_sorted_by_date" time="46.3530609608"/></testsuite>
# """
