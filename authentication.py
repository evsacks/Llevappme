import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyAuYV0KQbzAs9VNnTwKEOP8Uv0Q29xkiZE",
    'authDomain': "llevappme-jetl.firebaseapp.com",
    'databaseURL': "https://llevappme-jetl-default-rtdb.firebaseio.com",
    'projectId': "llevappme-jetl",
    'storageBucket': "llevappme-jetl.appspot.com",
    'messagingSenderId': "938379616472",
    'appId': "1:938379616472:web:9087b0cd87936374d937ad",
    'measurementId': "G-G0RXCFG1B4"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

