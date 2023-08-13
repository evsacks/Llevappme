import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyAuYV0KQbzAs9VNnTwKEOP8Uv0Q29xkiZE",
  'authDomain': "llevappme-jetl.firebaseapp.com",
  'projectId': "llevappme-jetl",
  'storageBucket': "llevappme-jetl.appspot.com",
  'messagingSenderId': "938379616472",
  'appId': "1:938379616472:web:11469ab6236530c8d937ad",
  'measurementId': "G-66J8QC1B3Q"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

