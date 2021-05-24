from sanic import Sanic
from sanic.response import json
import requests
app = Sanic("Switch")

@app.route("/post", methods=["POST"])
async def echo(request):
    if request.json:
        x=requests.post("http://165.227.125.50:8529/_db/_system/sensor/sensores", json=request.json)
        print(x)
        return json({"Respuesta":"Exitoso"})
    return json({"R": "No fue un json"})

@app.route("/get",methods=["GET"])
async def test(request):
   url = requests.get("http://165.227.125.50:8529/_db/_system/sensor/sensores")
   text = url.text
   print(text)
   return json(text)

if __name__ == "__main__":
  app.run(host="165.227.125.50", port=8001)
