from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import time
import psutil
import os
from datetime import datetime
from .models import Monitor
from urllib.parse import urlparse

#home page
def home2(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    response = requests.get('http://api.ipstack.com/'+ip+'?access_key=ee7d4335635d89a71b95dcc33eb2a044')
    rawData = response.json()
    continent = rawData['continent_name']
    country = rawData['country_name']
    capital = rawData['city']
    city = rawData['location']['capital']
    now = datetime.datetime.now()
    datetimenow = now.strftime("%Y-%m-%d %H:%M:%S")
    saveNow = Monitor(
        continent=continent,
        country=country,
        capital=capital,
        city=city,
        datetime=datetimenow,
        ip=ip
    )
    saveNow.save()
    return render(request, 'index2.html')

def home(request):
    return render(request, 'home.html')

#prometheus/pentest handler/view
def prometheus(request):
	return render(request, "pentest.html")

#not found
def notfound(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
   # return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip))
    message = "Page under Maintenance"
    context = {
		#"message": message,
		"ip": ip,
	}
    return render(request, "404.html", context)    


#choose account
def client(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
   # return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip))
    message = "Page under Maintenance"
    context = {
		#"message": message,
		"ip": ip,
	}
    return render(request, "client.html", context) 

#not found
def notfound(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
   # return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip))
    message = "Page under Maintenance"
    context = {
		#"message": message,
		"ip": ip,
	}
    return render(request, "404.html", context)    


#choose account
def scanner(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
   # return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip))
    message = "Page under Maintenance"
    context = {
		#"message": message,
		"ip": ip,
	}
    return render(request, "scanner.html", context)

def pentest(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        tobeScan = request.POST['url2']
        parsed = urlparse(tobeScan)
        if tobeScan.startswith('http'):
            parsedURL = parsed.netloc
        else:
            parsedURL = tobeScan
        print(parsedURL)
        #make request to api for xss
        url = 'https://http-observatory.security.mozilla.org/api/v1/analyze?host='+parsedURL
        r = requests.post(url)
        #raw = r['response_headers']['X-XSS-Protection']
        raw = r.json()
        #get scan id
        scannerId = str(raw['scan_id'])
        #get new test results
        url2 = 'https://http-observatory.security.mozilla.org/api/v1/getScanResults?scan='+scannerId
        r2 = requests.get(url2)
        raw2 = r2.json()
        #csp score description
        cspRaw = raw2.get('content-security-policy')
        cspClean = cspRaw.get('score_description')
        cspScore = cspRaw.get('score_modifier')

        #cookies
        cookieRaw = raw2.get('cookies')
        cookieClean = cookieRaw.get('score_description')
        cookieScore = cookieRaw.get('score_modifier')

        #cors
        corsRaw = raw2.get('cross-origin-resource-sharing')
        corsClean = corsRaw.get('score_description')
        corsScore = corsRaw.get('score_modifier')

        #public-key-pinning
        publicKey = raw2.get('public-key-pinning')
        publicKeyClean = publicKey.get('score_description')
        publicKeyScore = publicKey.get('score_modifier')

        #redirection
        redirectRaw = raw2.get('redirection')
        redirectClean = redirectRaw.get('score_description')
        redirectScore = redirectRaw.get('score_modifier')

        #referrer-policy
        referRaw = raw2.get('referrer-policy')
        referClean = referRaw.get('score_description')
        referScore = referRaw.get('score_modifier')

        #strict-transport-security
        strictRaw = raw2.get('strict-transport-security')
        strictClean = strictRaw.get('score_description')
        strictScore = strictRaw.get('score_modifier')

        #subresource-integrity
        subRaw = raw2.get('subresource-integrity')
        subClean = subRaw.get('score_description')
        subScore = subRaw.get('score_modifier')

        #x-content-type-options
        xRaw = raw2.get('x-content-type-options')
        xClean = xRaw.get('score_description')
        xScore = xRaw.get('score_modifier')

        #x-frame-options
        xFrameRaw = raw2.get('x-frame-options')
        xFrameRawClean = xFrameRaw.get('score_description')
        xFrameRawScore = xFrameRaw.get('score_modifier')

        #grades
        gradeRaw = raw.get('grade')
        #likelihood_indicator
        likRaw = raw.get('likelihood_indicator')

        #score
        scoreRAw = raw.get('score')
        #tests_passed
        testRaw = raw.get('tests_passed')
        #

        content = {
            "cspScore":cspScore,
            "cookieScore":cookieScore,
            "corsScore":corsScore,
            "publicKeyScore":publicKeyScore,
            "redirectScore":redirectScore,
            "referScore":referScore,
            "strictScore":strictScore,
            "subScore":subScore,
            "xScore":xScore,
            "xFrameRawScore":xFrameRawScore,
            "host":parsedURL,
            "cspDesc":cspClean,
            "cookies":cookieClean,
            "corsDesc":corsClean,
            "publicKeyClean":publicKeyClean,
            "redirectClean":redirectClean,
            "referClean":referClean,
            "strictClean":strictClean,
            "subClean":subClean,
            "xClean":xClean,
            "xFrameRawClean":xFrameRawClean,
            "gradeRaw":gradeRaw,
            "likelihood_indicator":likRaw,
            "scoreRAw":scoreRAw,
            "testRaw":testRaw,
        }
        return render(request, "pentestresult.html", content)
    return render(request, "webscanner.html")    


#xss scanner
class HelloView(APIView):
    def get(self, request):
        toScan = request.GET.get('url')
        parsed = urlparse(toScan)
        if toScan.startswith('http'):
            parsedURL = parsed.netloc
        else:
            parsedURL = toScan
        print(parsedURL)
        #make request to api for xss
        url = 'https://http-observatory.security.mozilla.org/api/v1/analyze?host='+parsedURL
        r = requests.post(url)
        #raw = r['response_headers']['X-XSS-Protection']
        raw = r.json()
        #get scan id
        scannerId = str(raw['scan_id'])
        #get new test results
        url2 = 'https://http-observatory.security.mozilla.org/api/v1/getScanResults?scan='+scannerId
        r2 = requests.get(url2)
        raw2 = r2.json()
        cleanedRaw = raw2.get('x-xss-protection')
        cleaned = bool(cleanedRaw.get('pass'))
        return Response(cleaned)


#xss scanner
class HelloWorldView(APIView):
    def get(self, request):
        toScan = request.GET.get('url')
        parsed = urlparse(toScan)
        if toScan.startswith('http'):
            parsedURL = parsed.netloc
        else:
            parsedURL = toScan
        print(parsedURL)
        #make request to api for xss
        url = 'https://http-observatory.security.mozilla.org/api/v1/analyze?host='+parsedURL
        r = requests.post(url)
        #raw = r['response_headers']['X-XSS-Protection']
        raw = r.json()
        #get scan id
        scannerId = str(raw['scan_id'])
        #get new test results
        url2 = 'https://http-observatory.security.mozilla.org/api/v1/getScanResults?scan='+scannerId
        r2 = requests.get(url2)
        raw2 = r2.json()
        #csp score description
        cspRaw = raw2.get('content-security-policy')
        cspClean = cspRaw.get('score_description')
        cspScore = cspRaw.get('score_modifier')

        #cookies
        cookieRaw = raw2.get('cookies')
        cookieClean = cookieRaw.get('score_description')
        cookieScore = cookieRaw.get('score_modifier')

        #cors
        corsRaw = raw2.get('cross-origin-resource-sharing')
        corsClean = corsRaw.get('score_description')
        corsScore = corsRaw.get('score_modifier')

        #public-key-pinning
        publicKey = raw2.get('public-key-pinning')
        publicKeyClean = publicKey.get('score_description')
        publicKeyScore = publicKey.get('score_modifier')

        #redirection
        redirectRaw = raw2.get('redirection')
        redirectClean = redirectRaw.get('score_description')
        redirectScore = redirectRaw.get('score_modifier')

        #referrer-policy
        referRaw = raw2.get('referrer-policy')
        referClean = referRaw.get('score_description')
        referScore = referRaw.get('score_modifier')

        #strict-transport-security
        strictRaw = raw2.get('strict-transport-security')
        strictClean = strictRaw.get('score_description')
        strictScore = strictRaw.get('score_modifier')

        #subresource-integrity
        subRaw = raw2.get('subresource-integrity')
        subClean = subRaw.get('score_description')
        subScore = subRaw.get('score_modifier')

        #x-content-type-options
        xRaw = raw2.get('x-content-type-options')
        xClean = xRaw.get('score_description')
        xScore = xRaw.get('score_modifier')

        #x-frame-options
        xFrameRaw = raw2.get('x-frame-options')
        xFrameRawClean = xFrameRaw.get('score_description')
        xFrameRawScore = xFrameRaw.get('score_modifier')

        #grades
        gradeRaw = raw.get('grade')
        #likelihood_indicator
        likRaw = raw.get('likelihood_indicator')

        #score
        scoreRAw = raw.get('score')
        #tests_passed
        testRaw = raw.get('tests_passed')
        #

        content = {
            "cspScore":cspScore,
            "cookieScore":cookieScore,
            "corsScore":corsScore,
            "publicKeyScore":publicKeyScore,
            "redirectScore":redirectScore,
            "referScore":referScore,
            "strictScore":strictScore,
            "subScore":subScore,
            "xScore":xScore,
            "xFrameRawScore":xFrameRawScore,
            "host":parsedURL,
            "cspDesc":cspClean,
            "cookies":cookieClean,
            "corsDesc":corsClean,
            "publicKeyClean":publicKeyClean,
            "redirectClean":redirectClean,
            "referClean":referClean,
            "strictClean":strictClean,
            "subClean":subClean,
            "xClean":xClean,
            "xFrameRawClean":xFrameRawClean,
            "gradeRaw":gradeRaw,
            "likelihood_indicator":likRaw,
            "scoreRAw":scoreRAw,
            "testRaw":testRaw,
        }
        return Response(content)
