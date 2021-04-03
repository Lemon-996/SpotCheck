from google.cloud import datastore

from send_sms import sendMessage
import yagmail
import re
import config as cf


# Have to also create a master entity


def Refresh(datastore_client):
    global client
    client = datastore_client
    updateMasterEntity()
    # UpdateUsers()
    # ClearCourses()


def updateMasterEntity():
    query = client.query(kind='masterEntity')
    ME = list(query.fetch())[0]
    ME[cf.dateObj.courseList] = []
    ME[cf.dateObj.emailsSent] = 0
    ME[cf.dateObj.textsSent] = 0
    client.put(ME)


def UpdateUsers():

    yag = yagmail.SMTP('spotcheckwes@gmail.com',
                       oauth2_file="oauth2_creds.json")
    welcomeBackMessage = "Hello SpotCheck Users! This month is the start of a new pre-reg period, and SpotCheck is once again open for business! To be alerted when a seat opens in a class you want during adjustment, simply go to https://spotcheck.space and sign up! The earlier you sign up, the quicker you'll be notified when a seat opens! All accounts are deleted each semester so you will have to sign up again. Love, SpotCheck"
    query = client.query(kind='user')
    results = list(query.fetch())
    for result in results:
        key = result.key
        username = result["username"]
        if re.search("\d{9,10}", username):  # Text
            sendMessage(username, welcomeBackMessage)
        elif re.search("@", username):  # Email
            yag.send(username, 'SpotCheck Is Now Active Again!',
                     welcomeBackMessage)
        client.delete(key)


def ClearCourses():
    query = client.query(kind='course')
    print('made it past query for all courses in clearcourses')
    print('made it past query key filter')
    results = list(query.fetch())
    for result in results:
        key = result.key
        client.delete(key)
