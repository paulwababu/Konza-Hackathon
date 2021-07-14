from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import datetime
import emoji
import random
import json
import dns
import dns.resolver
import phonenumbers
from phonenumbers import geocoder
import gtts
from playsound import playsound
import os
import subprocess
import sys
import netifaces
import psutil

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()
        
        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        responded = False

        #retrieve incoming cordinates and print on terminal
        lat, lon = request.POST.get('Latitude'), request.POST.get('Longitude')
        
        #retrieve incoming image
        media = request.POST.get('MediaContentType0', '')
        

        if incoming_msg == 'hello':
            response = emoji.emojize("""
*Hi! I am Prometheus* :wink:
It's a pleasure to make your acquaintance :wave:
You can give me the following commands:
:black_small_square: *'pentest':* Discover common web application vulnerabilities and server configuration issues! :rocket:
:black_small_square: *'paul'*: See a picture of my creator? :superhero:
:black_small_square: *'resolve <domain name>'*: Find the IP address of the Domain name eg "resolve tutorialspoint.com" :alien:
:black_small_square: *'trace <phonenumber>'*: Trace origin of phone number eg "trace +254797584194" :handshake:
:black_small_square: *'instagram <username>'*: Retrieve publicly-available Instagram Profile. That includes name, bio, followers information along with profile pictures eg "instagram xtiandela":winking face:
:black_small_square: *'news'*: Latest news from around the world. :newspaper:
:black_small_square: *'recipe'*: Searches Allrecipes.com for the best recommended recipes. :fork_and_knife:
:black_small_square: *'recipe <query>'*: Searches Allrecipes.com for the best recipes based on your query. :mag:
:black_small_square: *'get recipe'*: Run this after the 'recipe' or 'recipe <query>' command to fetch your recipes! :stew:
:black_small_square: *'statistics <country>'*: Show the latest COVID19 statistics for each country. :earth_americas:
:black_small_square: *'statistics <prefix>'*: Show the latest COVID19 statistics for all countries starting with that prefix. :globe_with_meridians:
""", use_aliases=True)
            msg.body(response)
            responded = True
        elif incoming_msg == 'paul':
            # return his pic
            msg.media('https://icomnalt.sirv.com/Images/paul.jpg')
            msg.body("Connect on Linked in: https://www.linkedin.com/in/paul-wababu-660b511a7/")
            responded = True

        elif lat and lon:
            # return geo cordinates
            msg.body(lat + "\n" + lon)
            responded = True    

        elif media:
            #get image sent
            msg.body(media)
            print(media)
            responded = True

        elif incoming_msg.startswith('resolve'):
            search_textt = incoming_msg.replace('resolve', '')
            search_textt = search_textt.strip()
            result = dns.resolver.query(search_textt, 'A')
            for ipval in result:
                ip = ipval.to_text()
                #print("IP", ipval.to_text())
                msg.body(ip)
                msg.body("Happy Hacking!")
            #msg.body("Enter Domain name to resolve: eg tutorialspoint.com")
            # return a cat pic
            #msg.media('https://cataas.com/cat')
            
            responded = True


        elif incoming_msg.startswith('instagram'):
            search_textt = incoming_msg.replace('instagram', '')
            search_textt = search_textt.strip()
            username = search_textt
            url = "https://easy-instagramapi.p.rapidapi.com/v1/profile/"+username
            headers = {
                'x-rapidapi-key': "43628cd680msh1812b1660500eb7p182976jsn5dda2f77f08f",
                'x-rapidapi-host': "easy-instagramapi.p.rapidapi.com"
     
            }
            response = requests.request("GET", url, headers=headers)
            a = response.json()
            print(a)
            dp = a['profilePhotoHd']
            followers = str(a['followersCount'])
            following = str(a['followingCount'])
            msg.media(dp)
            msg.body("Instagram User: " +username)
            msg.body("Total Followers: " +followers)
            msg.body("Total Following: " +following)
            msg.body("Bio: " +a['biography'])
            responded = True    
            

        elif incoming_msg.startswith('trace'):
            search_textt = incoming_msg.replace('trace', '')
            search_textt = search_textt.strip()
            phone_number1 = phonenumbers.parse(search_textt)
            location = geocoder.description_for_number(phone_number1,'en')
            msg.body("Phone number originates from: ")
            msg.body(location)
            
            responded = True

        elif incoming_msg == 'quote':
            # returns a quote
            r = requests.get('https://api.quotable.io/random')

            if r.status_code == 200:
                data = r.json()
                quote = f'{data["content"]} ({data["author"]})'

            else:
                quote = 'I could not retrieve a quote at this time, sorry.'

            msg.body(quote)
            responded = True

        elif incoming_msg == 'cat':
            # return a cat pic
            msg.media('https://cataas.com/cat')
            responded = True



        elif incoming_msg == 'dog':
            # return a dog pic
            r = requests.get('https://dog.ceo/api/breeds/image/random')
            data = r.json()
            msg.media(data['message'])
            responded = True

        elif incoming_msg.startswith('recipe'):

            # search for recipe based on user input (if empty, return featured recipes)
            search_text = incoming_msg.replace('recipe', '')
            search_text = search_text.strip()
            
            data = json.dumps({'searchText': search_text})
            
            result = ''
            # updates the Apify task input with user's search query
            r = requests.put('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/input?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1', data = data, headers={"content-type": "application/json"})
            if r.status_code != 200:
                result = 'Sorry, I cannot search for recipes at this time.'

            # runs task to scrape Allrecipes for the top 5 search results
            r = requests.post('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')
            if r.status_code != 201:
                result = 'Sorry, I cannot search Allrecipes.com at this time.'

            if not result:
                result = emoji.emojize("I am searching Allrecipes.com for the best {} recipes. :fork_and_knife:".format(search_text),
                                        use_aliases = True)
                result += "\nPlease wait for a few moments before typing 'get recipe' to get your recipes!"
            msg.body(result)
            responded = True

        #pentest tool
        elif incoming_msg.startswith('xss'):

            # search for recipe based on user input (if empty, return featured recipes)
            urlToScan = incoming_msg.replace('xss', '')
            scannedClean = urlToScan.strip()
            url = 'https://http-observatory.security.mozilla.org/api/v1/analyze?host='+scannedClean+'&rescan=true'
            r = requests.post(url)
            #raw = r['response_headers']['X-XSS-Protection']
            raw = r.json()
            print(raw)
            cleaned = raw.get('response_headers', {})
            cleanRaw = cleaned.get('X-XSS-Protection', None)
            if cleanRaw == "1; mode=block":
                xss = False
                result = "X-XSS-Protection header implemented"
            elif cleaned == {}:
                errorDisplay = raw.get('error')
                xss = errorDisplay
                result = xss
            elif cleanRaw == {}:
                xss = True
                result = "X-XSS-Protection header not implemented"
            else:
                result = "X-XSS-Protection header not implemented"
            msg.body(result)
            responded = True

        elif incoming_msg.startswith('pentest'):

            # search for recipe based on user input (if empty, return featured recipes)
            urlToScan = incoming_msg.replace('pentest', '')
            scannedClean = urlToScan.strip()
            url = 'https://http-observatory.security.mozilla.org/api/v1/analyze?host='+scannedClean
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
            #result = content
            msg.body("V͇u͇l͇n͇e͇r͇a͇b͇i͇l͇i͇t͇y͇ R͇e͇p͇o͇r͇t͇" + "\n" + "\n" + "Host: " +scannedClean + "\n" + "\n" + cookieClean + "\n" + "\n" + corsClean + "\n" + "\n" + publicKeyClean + "\n" + "\n" + redirectClean + "\n" + "\n" + referClean + "\n" + "\n" + strictClean + "\n" + "\n" + subClean + "\n" + "\n" + xClean + "\n" + "\n" + xFrameRawClean + "\n" + "\n" + "Exploit Likelyhood: " + likRaw + "\n" + "\n" + "Grade: " + str(gradeRaw) + "\n" + "\n" + "Score: " + str(scoreRAw)+"/100")
            responded = True      


        elif incoming_msg == 'todo':
            #get todo list for the day
            todoRequest = requests.get('http://127.0.0.1:8000/api/v1/todo')
            todoClean = todoRequest.json()
            todoCleanRaw = todoClean.get('results')
            for data2 in todoCleanRaw:
                msg.body(str(data2.get('title')))
            #msg.body(data2)
            responded = True


        elif incoming_msg.startswith('action'):
            #get action to be added on todo list
            print(incoming_msg.split())
            msg.body("Check terminal")
            responded = True
   

        elif incoming_msg.startswith('ping'):
            toPing = incoming_msg.split()
            toPingClean = toPing[1] #site to be pinged
            toPingTimes = toPing[2] #number of packets
            responsePing = subprocess.check_output(['ping ' +toPingClean+ ' -c '+(toPingTimes)], shell=True)
            msg.body(responsePing.decode("utf-8"))
            responded = True

        elif incoming_msg.startswith('cpu'):
            load1, load5, load15 = psutil.getloadavg()
            cpu_usage = int((load15/os.cpu_count()) * 100)
            ram_usage = int(psutil.virtual_memory()[2])
            msg.body(cpu_usage + ram_usage)
            responded = True

        elif incoming_msg.startswith('api'):
            toRequest = incoming_msg.split()
            requestMake = toRequest[1] #api to be pinged
            requestMade = requests.get(requestMake)
            requestResponse = requestMade.text
            msg.body(requestResponse)
            responded = True        

        elif incoming_msg == 'get recipe':
            # get the last run details
            r = requests.get('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs/last?token=qTt3H59g5qoWzesLWXeBKhsXu')
            
            if r.status_code == 200:
                data = r.json()

                # check if last run has succeeded or is still running
                if data['data']['status'] == "RUNNING":
                    result = 'Sorry, your previous query is still running.'
                    result += "\nPlease wait for a few moments before typing 'get recipe' to get your recipes!"

                elif data['data']['status'] == "SUCCEEDED":

                    # get the last run dataset items
                    r = requests.get('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')
                    data = r.json()

                    if data:
                        result = ''

                        for recipe_data in data:
                            url = recipe_data['url']
                            name = recipe_data['name']
                            rating = recipe_data['rating']
                            rating_count = recipe_data['ratingcount']
                            prep = recipe_data['prep']
                            cook = recipe_data['cook']
                            ready_in = recipe_data['ready in']
                            calories = recipe_data['calories']

                            result += """
*{}*
_{} calories_
Rating: {:.2f} ({} ratings)
Prep: {}
Cook: {}
Ready in: {}
Recipe: {}
""".format(name, calories, float(rating), rating_count, prep, cook, ready_in, url)

                    else:
                        result = 'Sorry, I could not find any results for {}'.format(search_text)

                else:
                    result = 'Sorry, your previous search query has failed. Please try searching again.'

            else:
                result = 'I cannot retrieve recipes at this time. Sorry!'

            msg.body(result)
            responded = True

        elif incoming_msg == 'news':
            r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news,the-washington-post,the-wall-street-journal,cnn,fox-news,cnbc,abc-news,business-insider-uk,google-news-uk,independent&apiKey=3ff5909978da49b68997fd2a1e21fae8')
            
            if r.status_code == 200:
                data = r.json()
                articles = data['articles'][:5]
                result = ''
                
                for article in articles:
                    title = article['title']
                    url = article['url']
                    if 'Z' in article['publishedAt']:
                        published_at = datetime.datetime.strptime(article['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
                    else:
                        published_at = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                    result += """
*{}*
Read more: {}
_Published at {:02}/{:02}/{:02} {:02}:{:02}:{:02} UTC_
""".format(
    title,
    url, 
    published_at.day, 
    published_at.month, 
    published_at.year, 
    published_at.hour, 
    published_at.minute, 
    published_at.second
    )

            else:
                result = 'I cannot fetch news at this time. Sorry!'

            msg.body(result)
            responded = True

        elif incoming_msg.startswith('statistics'):
            # runs task to aggregate data from Apify Covid-19 public actors
            requests.post('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/run-sync?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')
            
            # get the last run dataset items
            r = requests.get('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')
            
            if r.status_code == 200:
                data = r.json()

                country = incoming_msg.replace('statistics', '')
                country = country.strip()
                country_data = list(filter(lambda x: x['country'].lower().startswith(country), data))

                if country_data:
                    result = ''

                    for i in range(len(country_data)):
                        data_dict = country_data[i]
                        last_updated = datetime.datetime.strptime(data_dict.get('lastUpdatedApify', None), "%Y-%m-%dT%H:%M:%S.%fZ")

                        result += """
*Statistics for country {}*
Infected: {}
Tested: {}
Recovered: {}
Deceased: {}
Last updated: {:02}/{:02}/{:02} {:02}:{:02}:{:03} UTC
""".format(
    data_dict['country'], 
    data_dict.get('infected', 'NA'), 
    data_dict.get('tested', 'NA'), 
    data_dict.get('recovered', 'NA'), 
    data_dict.get('deceased', 'NA'),
    last_updated.day,
    last_updated.month,
    last_updated.year,
    last_updated.hour,
    last_updated.minute,
    last_updated.second
    )
                else:
                    result = "Country not found. Sorry!"
            
            else:
                result = "I cannot retrieve statistics at this time. Sorry!"

            msg.body(result)
            responded = True
    
        elif incoming_msg.startswith('meme'):
            r = requests.get('https://www.reddit.com/r/memes/top.json?limit=20?t=day', headers = {'User-agent': 'your bot 0.1'})
            
            if r.status_code == 200:
                data = r.json()
                memes = data['data']['children']
                random_meme = random.choice(memes)
                meme_data = random_meme['data']
                title = meme_data['title']
                image = meme_data['url']

                msg.body(title)
                msg.media(image)
            
            else:
                msg.body('Sorry, I cannot retrieve memes at this time.')

            responded = True   

        if not responded:
            url = "https://robomatic-ai.p.rapidapi.com/api.php"

            payload = "key=RHMN5hnQ4wTYZBGCF3dfxzypt68rVP&cbid=1&ChatSource=RapidAPI&SessionID=RapidAPI1&cbot=1&op=in&in="+incoming_msg
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'x-rapidapi-key': "43628cd680msh1812b1660500eb7p182976jsn5dda2f77f08f",
                'x-rapidapi-host': "robomatic-ai.p.rapidapi.com"
                }

            responseROBO = requests.request("POST", url, data=payload, headers=headers)
            answer = responseROBO.json()
            answerw = answer.get('out')
            msg.body(answerw)
        return HttpResponse(str(resp))