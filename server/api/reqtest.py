from requests import get,post

url='http://127.0.0.1:8000/api/test/'
data=get(url,params={
    'c':'d'
})
print(data)