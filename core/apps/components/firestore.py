
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin import firestore
cred = credentials.Certificate("Key.json")
firebase_admin.initialize_app(cred)


db = firestore.client()


def adduser_firestore(id , email , name , avatar , type  ):
    db.collection('users').document(email).set({ 'id':id , 'email' :email , 'name' : name , 'avatar' : avatar , 'type' : type })

# def addDoctor_firestore(email , name , city , mobile , start , end  ):
#     db.collection('Doctor').document(email).set({ 'name':name , 'mobile':mobile , 'city' :city , 'start_work' : start , 'end_work' :end })





