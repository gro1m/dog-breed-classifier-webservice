import requests
url = "http://localhost:5000/upload"
with open("tests/images/animal-dog-pet-brown.jpeg", 'rb') as f:
    files = {'file': f}

print("Read file; sending POST request")
r = requests.post(url=url,files=files)