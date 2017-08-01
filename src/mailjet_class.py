from prometheus_client.core import GaugeMetricFamily
from prometheus_client.core import CounterMetricFamily

import json, requests, sys, os, ast, signal, datetime

import logging, socket, ssl


import requests
import re

class MailjetCollector(object):

  def __init__(self, api_key_private, api_key_public):
        """ initializing attributes"""
        self.api_key_private = api_key_private
        self.api_key_public = api_key_public
        self.METRIC_PREFIX = 'mailjet_info_'

        self.api = 'https://api.mailjet.com'
        self.endpoint = '/v3/REST/messagestatistics'

  def convertCamelToSnake(self, name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

  def collect(self):

    metric_description = 'Mailjet number %s' 

    now = datetime.datetime.utcnow()
    now_minus_delta = now - datetime.timedelta(minutes = 5)
    dateTimeRqFormat = '%Y-%m-%dT%H:%M:00+00:00'
    print( now.strftime(dateTimeRqFormat) )
    print( now_minus_delta.strftime(dateTimeRqFormat))

    payload = {'FromTS': now_minus_delta.strftime(dateTimeRqFormat) , 'ToTS': now.strftime(dateTimeRqFormat)} 
    r = requests.get(self.api + self.endpoint , params=payload, auth=(self.api_key_public, self.api_key_private))

    datas = r.json()['Data']

    for data in datas:
        for attribute, value in data.items():

            name_attribute = self.convertCamelToSnake(attribute)

            gauge = GaugeMetricFamily(self.METRIC_PREFIX + name_attribute, metric_description % name_attribute, value=value)

            yield gauge
    


    # get total for the day

    today = datetime.date.today()
    begintime = today.strftime("%Y-%m-%dT00:00:00+00:00")
    endtime = today.strftime("%Y-%m-%dT23:59:59+00:00")

    print( begintime )
    print( endtime)

    payload = {'FromTS': begintime , 'ToTS': endtime} 
    r = requests.get(self.api + self.endpoint , params=payload, auth=(self.api_key_public, self.api_key_private))

    datas = r.json()['Data']

    for data in datas:
        for attribute, value in data.items():

            name_attribute = self.convertCamelToSnake(attribute)

            counter = CounterMetricFamily(self.METRIC_PREFIX + 'daily_' + name_attribute, metric_description % name_attribute, value=value)

            yield counter
