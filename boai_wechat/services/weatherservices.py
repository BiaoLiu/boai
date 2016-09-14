#! /usr/bin/env python
# coding=utf-8

import requests
import json


class _cityWeather():

    #key
    appkey='7ed5edfdb07013922a47bd2fbf194d3d'
    #url
    appurl='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=7ed5edfdb07013922a47bd2fbf194d3d'

    def __init__(self):
        pass

    def getcitynamebyip(self,ip):

        pass

    def getcityweather(self,cityname='合肥'):
        requrl=self.appurl % (cityname,)
        r =  requests.get(requrl)
        return r.text

cityweather = _cityWeather()


if __name__ =="__main__":


    print (cityweather.getcityweather('合肥'))