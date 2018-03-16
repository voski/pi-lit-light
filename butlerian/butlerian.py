"""
Butlerian

A convenient way to query the Jenkins build status of an app.
"""

import urllib
import urllib2
import xml.etree.ElementTree as ElementTree

# Querying Jenkins XML API:
# https://stackoverflow.com/questions/38534171/how-to-find-and-query-a-specific-build-in-jenkins-using-the-python-jenkins-api
#
# Useful query for Clover's Jenkins setup:
# http://jenkins.corp.clover.com:8080/job/build-apps-apk/api/xml?depth=2&xpath=//fullDisplayName[contains(text(),%27tables2%27)]/parent::*&wrapper=appBuilds


_JENKINS_URL = 'http://jenkins.corp.clover.com:8080'


class JenkinsApi(object):

    def __init__(self, base_url=_JENKINS_URL):
        self.base_url = base_url

    def _get_xml_api(self, job_name):
        return "{}/job/{}/api/xml".format(self.base_url, job_name)

    @classmethod
    def _get_xpath_expr(cls, app_name):
        # FIXME: might be a way to query based on parameters instead of fullDisplayName?
        return "//fullDisplayName[contains(text(),'{}')]/parent::*".format(app_name)

    def get_job(self, job_name, app_name_filter, depth=2):
        if app_name_filter:
            params = {'depth': depth, 'xpath': self._get_xpath_expr(app_name_filter),
                      'wrapper': 'appBuilds'}
        else:
            params = {'depth': depth}

        # FIXME: there's must be a nicer way to build this URL
        url = self._get_xml_api(job_name) + '?' + urllib.urlencode(params)
        response = urllib2.urlopen(url)
        return Job(response.read())


class Build(object):
    parameters = {}

    def __init__(self, xml_element):
        # Parse build parameters
        for param in xml_element.iter('parameter'):
            key = param.find('name').text
            value = param.find('value').text
            self.parameters[key] = value

        self.id = int(xml_element.find('id').text)
        self.full_display_name = xml_element.find('fullDisplayName').text
        self.building = bool(xml_element.find('building').text)
        self.result = xml_element.find('result').text

    def __str__(self):
        return "Build(id={}, full_display_name={}, building={}, result={})".format(
            self.id, self.full_display_name, self.building, self.result
        )

    def __cmp__(self, other):
        return cmp(self.id, other.id)


class Job(object):
    builds = []

    def __init__(self, xml_str):
        root = ElementTree.fromstring(xml_str)
        for element in root.iter('build'):
            self.builds.append(Build(element))
        self.builds.sort()

    def __str__(self):
        return "Job(builds={})".format([str(e) for e in self.builds])
