from rest_framework import response 
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from .processing import processTime, processingEventData
import requests
import pymongo

connection_String  = "mongodb+srv://KeshavMehta:ftZbEq1LCpPW4Uy1@cluster0.gq0hrfm.mongodb.net/?retryWrites=true&w=majority"
my_client = pymongo.MongoClient(connection_String)
dbname = my_client['test']
collection_name = dbname["users"]
myuser = {'email': 'keshav.mehta@student.csulb.edu'}
mydoc = collection_name.find(myuser)
a = list(mydoc)


@api_view(['GET'])
def getPinList(request):
    query = {'email': request.GET.get('query')}
    user = collection_name.find(query)
    if(user):
        pinnedEvents = list(user)[0]['Pinned']
        return response.Response(pinnedEvents)
    return response.Response("USER NOT FOUND")

@api_view(['GET'])
def getSubList(request):
    query = {'email': request.GET.get('query')}
    user = collection_name.find(query)
    print(user)
    if(user):
        subscribedOrgs = list(user)[0]['Subscribed']
        print(subscribedOrgs)
        return response.Response(subscribedOrgs)
    print("DID NOT FIND USER______________")
    return response.Response("USER NOT FOUND")

def date(date):
        final_date = ""
        if(int(date[:2]) >= 13):
            for i in range(13,25):
                if(i == int(date[:2])):
                    final_date = i-12
                    date = str(final_date) + " : " + date[3:] + " pm"
                    return date
        else:
            return  date + " am"
        
def month(month):
    table = {"01":"January",
            "02":"February",
            "03":"March",
            "04":"April",
            "05":"May",
            "06":"June",
            "07":"July",
            "08":"August",
            "09":"September",
            "10":"October",
            "11":"November",
            "12":"December"
            }
    if month[5:7] in table:
        return f"{table[month[5:7]]} {month[8:10]} {month[0:4]}"


@api_view(['GET'])
def getEvents(request):
    
                        #https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter=2023-10-11T17%5E%25%5E3A39%5E%25%5E3A12-07%5E%25%5E3A00&status=Approved&take=15&query=farm
    res = (requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter={processTime()}&status=Approved&take=10&query={request.GET.get('query')}")).json()['value']
    # print(res)
    val  = [ {"pinned":False,'name': i['name'], "key" : i['id'], 'description': processingEventData(i['description']) , 'location': i['location'],'start' : f"{date(i['startsOn'][11:16])} on {month(i['startsOn'][:10])}", 'end': f"{date(i['endsOn'][11:16])} on {month(i['endsOn'][:10])}", 'imagePath': f'https://se-images.campuslabs.com/clink/images/{i["imagePath"]}?preset=large-w&quot'} for i in res]
    # print(val)

    return response.Response(val)

# get orgs list by username form front end and for every orgID do getORGcall from the beach sync database
@api_view(['GET'])
def getOrgs(request):
    res = requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/search/organizations?orderBy%5B0%5D=UpperName%20asc&top=10&filter&query={request.GET.get('query')}&skip=0").json()['value']

    val  = [ { 'subscribed': False, 'key': i['Id'], 'name': i['Name'], 'Summary': i['Summary'], 'ProfilePicture': f"https://se-images.campuslabs.com/clink/images/{i['ProfilePicture']}?preset=small-sq"} for i in res]
    
    return response.Response(val)

# image query https://se-images.campuslabs.com/clink/images/__profilepicture__?preset=small-sq
@api_view(['GET'])
def getOrgEvents(request):                                                              
   # https://csulb.campuslabs.com/engage/api/discovery/event/search?filter=EndsOn%20ge%202023-12-10T03%3A24%3A50-08%3A00&top=4&orderBy%5B0%5D=EndsOn%20asc&endsAfter=2023-12-10T03%3A24%3A49-08%3A00&orderByField=endsOn&orderByDirection=ascending&status=Approved&take=4&organizationIds%5B0%5D=215692&excludeIds%5B0%5D=9653925
    # https://csulb.campuslabs.com/engage/api/discovery/event/search?filter=EndsOn%20ge%202023-12-10T03%3A24%3A50-08%3A00&top=4&orderBy%5B0%5D=EndsOn%20asc&endsAfter=2023-12-10T03%3A24%3A49-08%3A00&orderByField=endsOn&orderByDirection=ascending&status=Approved&take=4&organizationIds%5B0%5D=215692&excludeIds%5B0%5D=9653925
    time = processTime()
    res = requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/search?filter=EndsOn%20ge%20{time}&top=4&orderBy%5B0%5D=EndsOn%20asc&endsAfter={time}&orderByField=endsOn&orderByDirection=ascending&status=Approved&take=4&organizationIds%5B0%5D={request.GET.get('query')}&excludeIds%5B0%5D=9653925").json()['value']
    val  = [ {"pinned":False,'name': i['name'], "key" : i['id'], 'description': processingEventData(i['description']) , 'location': i['location'],'start' : f"{date(i['startsOn'][11:16])} on {month(i['startsOn'][:10])}", 'end': f"{date(i['endsOn'][11:16])} on {month(i['endsOn'][:10])}", 'imagePath': f'https://se-images.campuslabs.com/clink/images/{i["imagePath"]}?preset=large-w&quot'} for i in res]
    return response.Response(val)
@api_view(['GET'])
def getEventById(request):
    print("MC____________BC")
    # https://csulb.campuslabs.com/engage/api/discovery/event/9634061
    res = requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/{request.GET.get('query')}").json()
    print(res['address']['name'])
    val  = [ {"pinned":False,'name': i['name'], "key" : i['id'], 'description': processingEventData(i['description']) , 'location': i['address']['name'],'start' : f"{date(i['startsOn'][11:16])} on {month(i['startsOn'][:10])}", 'end': f"{date(i['endsOn'][11:16])} on {month(i['endsOn'][:10])}", 'imagePath': i["imageUrl"]} for i in res]
    return response.Response(val)