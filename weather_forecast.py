from flask import Flask,jsonify,request 
from flask import render_template
import requests

web=Flask(__name__)

key="a7838e44bdc9eceede85cfba8812aba5"
url="https://api.openweathermap.org/data/2.5/weather"

def direction(degs):
    """ it convert degree into direction because thorugh api we get degress"""

    if 0 <= degs < 22.5 or degs >= 337.5:
        return "North (N)"
    elif 22.5 <= degs < 67.5:
        return "North-East (NE)"
    elif 67.5 <= degs < 112.5:
        return "East (E)"
    elif 112.5 <= degs < 157.5:
        return "South-East (SE)"
    elif 157.5 <= degs < 202.5:
        return "South (S)"
    elif 202.5 <= degs < 247.5:
        return "South-West (SW)"
    elif 247.5 <= degs < 292.5:
        return "West (W)"
    elif 292.5 <= degs < 337.5:
        return "North-West (NW)"



@web.route("/")
def home():
    return render_template("index.html")

@web.route("/get_update",methods=["POST"])
def result():
    city=request.form["city"]
    country=request.form["country"]
    
    params = {
        "q": f"{city},{country}",
        "appid": key,
        "units": "metric"
    }
    #making api request
    response=requests.get(url,params=params)
    value=response.json()
    
    if response.status_code==200:
        temp_cel=value["main"]["temp"]
        temp_far= (temp_cel * 9/5) + 32
        wind_dir=value["wind"]["deg"]
        

        weather= {
            "temperature": temp_cel,
            "temp_far": int(temp_far), #farnhite 
            "weather": value["weather"][0]["description"],
            "wind_speed": value["wind"]["speed"],
            "humidity":value["main"]["humidity"],
            "wind_dir":direction(wind_dir)
            }
        return jsonify(weather)
    elif response.status_code==500:
        return jsonify({"error":"API FAILURE"})
    
    elif response.status_code==404:
        return jsonify({"error":"Invalid details"})
    else:
        return jsonify({"error":"Something went wrong, pls try again!"})

if __name__ == "__main__":
 web.run(debug=True,port=5000)
