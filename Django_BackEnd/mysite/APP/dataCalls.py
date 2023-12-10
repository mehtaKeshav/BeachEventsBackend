from rest_framework import response 
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from .processing import processTime, processingEventData
import requests

# <<<<<<< HEAD
# Search by IDs 
# @api_view(['GET'])
# def getEvents(request):
#     print("pappu:", request.GET.get('query'))
#     if request.GET.get('query') != None:
#         print(processTime())
#         res = (requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter={processTime()}&status=Approved&take=10000000&query={request.GET.get('query')}")).json()['value']
#     else:
#          res = (requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter={processTime()}&status=Approved&take=10000000")).json()['value']

#     val  = [ {'name': i['name'], "Id" : i['id'], 'description': i['description'], 'location': i['location'],'start' : i['startsOn'], 'end': i['endsOn']} for i in res]
#     return response.Response(val)

# @api_view(['GET'])
# def getEvents(request):
#                         #https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter=2023-10-11T17%5E%25%5E3A39%5E%25%5E3A12-07%5E%25%5E3A00&status=Approved&take=15&query=farm
#     res = (requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter={processTime()}&status=Approved&take=100000&query={request.GET.get('query')}")).json()['value']
#     val  = [ { 'pinned': False,'name': i['name'], "key" : i['id'], 'description': processingEventData(i['description']) , 'location': i['location'],'start' : i['startsOn'], 'end': i['endsOn'], 'imagePath': f'https://se-images.campuslabs.com/clink/images/{i["imagePath"]}?preset=large-w&quot'} for i in res]

@api_view(['GET'])
def getEvents(request):
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
                        #https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter=2023-10-11T17%5E%25%5E3A39%5E%25%5E3A12-07%5E%25%5E3A00&status=Approved&take=15&query=farm
    res = (requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/event/search?endsAfter={processTime()}&status=Approved&take=10&query={request.GET.get('query')}")).json()['value']
    print(res)
    val  = [ {"pinned":False,'name': i['name'], "Id" : i['id'], 'description': processingEventData(i['description']) , 'location': i['location'],'start' : f"{date(i['startsOn'][11:16])} on {month(i['startsOn'][:10])}", 'end': f"{date(i['endsOn'][11:16])} on {month(i['endsOn'][:10])}", 'imagePath': f'https://se-images.campuslabs.com/clink/images/{i["imagePath"]}?preset=large-w&quot'} for i in res]
    print(val)
# >>>>>>> feeab12b92b0d71a478f3d7fc9eb99ffd0d76b0a
    return response.Response(val)

# get orgs list by username form front end and for every orgID do getORGcall from the beach sync database
@api_view(['GET'])
def getOrgs(request):
    res = requests.get(f"https://csulb.campuslabs.com/engage/api/discovery/search/organizations?orderBy%5B0%5D=UpperName%20asc&top=10&filter&query={request.GET.get('query')}&skip=0").json()['value']
# <<<<<<< HEAD
    # return response.Response(res.json()['value'])
    val  = [ { 'subscribed': False, 'key': i['Id'], 'name': i['Name'], 'Summary': i['Summary'], 'ProfilePicture': f"https://se-images.campuslabs.com/clink/images/{i['ProfilePicture']}?preset=small-sq"} for i in res]
    
# =======
#     val  = [ {'name': i['Name'], 'Summary': i['Summary'], 'ProfilePicture': f"https://se-images.campuslabs.com/clink/images/{i['ProfilePicture']}?preset=small-sq"} for i in res]
# >>>>>>> feeab12b92b0d71a478f3d7fc9eb99ffd0d76b0a
    return response.Response(val)

# image query https://se-images.campuslabs.com/clink/images/__profilepicture__?preset=small-sq
@api_view(['GET'])
def getOrgEvents(request):
    pass

