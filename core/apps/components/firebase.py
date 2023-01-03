import pyrebase



firebaseConfig = {
  'apiKey': "AIzaSyBieYFF0MbSnxRde82anPnkxJ4jyriAz2o",
  'authDomain': "gradproject-6d49d.firebaseapp.com",
 'projectId': "gradproject-6d49d",
  'storageBucket': "gradproject-6d49d.appspot.com",
  'messagingSenderId': "762585809218",
  'appId': "1:762585809218:web:c1918968e3ede4256588db",
  'measurementId': "G-C94BX84X6Z" , 
  "databaseURL": ""

}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


def firebase_auth (email ,password):
   
       auth.create_user_with_email_and_password(email ,password)


import firebase_admin
from firebase_admin import credentials , messaging
from firebase_admin import firestore
cred = credentials.Certificate("Key.json")
firebase_admin.initialize_app(cred)


db = firestore.client()


def adduser_firestore(id , email , name , avatar , type  ):
    db.collection('users').document(email).set({ 'id':id , 'email' :email , 'name' : name , 'avatar' : avatar , 'type' : type })


def signup_firebase(email ,password ,id , name , avatar , type ):
  firebase_auth(email=email , password= password)
  adduser_firestore(id=id , email=email , name=name ,avatar=avatar  ,type=type)

  
def fireauth_login (email , password)  :
  try : 
    user= auth.sign_in_with_email_and_password(email=email , password=password)
    
    return (user['email'])

  except : 
    print('error auth')


def firebase_login(email , password) : 

  user_email= fireauth_login(email=email , password=password)
  user_data = db.collection('users').document(user_email).get()
  return (user_data.to_dict())


def firebase_chat (sender , receiver , time , text  ):
   db.collection('users').document(sender).collection('chats').document(receiver).collection('messages').add({
'sender' : sender , 'receiver' :receiver , 'time' :time , 'text' :text

  })

   db.collection('users').document(receiver).collection('chats').document(sender).collection('messages').add({
'sender' : sender , 'receiver' :receiver , 'time' :time , 'text' :text

  })
 




def sendPush(title, msg, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    #print('Successfully sent message:', response)


def firebase_sendNotification(title, msg, token):
  sendPush(msg=msg , title=title ,registration_token=list(token))
  
 
  








#firebase_login('hellodoctor1121@gmail.com' , '20012001')


