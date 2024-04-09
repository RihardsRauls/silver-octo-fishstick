from flask import(
    Flask,
    render_template,
    request
)
from requests import get

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/get_weather", methods=["GET", "POST"])
def get_weather():
    if request.method == "POST":
        api_key=""

        city = request.form.get('city')

        option = request.form.get('option')

        if option == "1":
            # print(city)

            geo_urla = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"

            req = get(geo_urla)

            if req.status_code !=200:
                return render_template("layout.html", text = "هناك خطأ ما")
            # print(req)
            # print(req.json())

            try: 
                geo_data = req.json()[0]
            except:
                return render_template("layout.html", text = "هناك خطأ ما")

            lat = geo_data["lat"]
            lon = geo_data["lon"]

        
            witcher_urla = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=pl&appid={api_key}"

            req = get(witcher_urla)

            if req.status_code !=200:
                return render_template("layout.html", text = "هناك خطأ ما")
            
            try: 
                witcher_data = req.json()
            except:
                return render_template("layout.html", text = "هناك خطأ ما")

            temp = [float(witcher_data["main"]["temp"])]
            desc = [witcher_data["weather"][0]["description"]]
            icon = witcher_data["weather"][0]["icon"]
            icon_url = [f"https://openweathermap.org/img/wn/{icon}@2x.png"]

            # if polska, then i get name, if not then i get the default name
            try:
                name = geo_data["local_names"]["pl"]
            except:
                name = geo_data["name"]

            # print(witcher_data)
            # print(temp, desc, name)

            weather = {
                "temperature": temp, 
                "description" : desc, 
                "icon" : icon_url, 
                "cityname" : name
            }
            
            return render_template('layout.html', weather=weather)
        if option == "5":

            geo_urla = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"

            req = get(geo_urla)

            if req.status_code !=200:
                return render_template("layout.html", text = "هناك خطأ ما")

            try: 
                geo_data = req.json()[0]
            except:
                return render_template("layout.html", text = "هناك خطأ ما")

            lat = geo_data["lat"]
            lon = geo_data["lon"]

            try:
                name = geo_data["local_names"]["pl"]
            except:
                name = geo_data["name"]
                    

        
            witcher_urla = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=pl&appid={api_key}"

            req = get(witcher_urla)

            if req.status_code !=200:
                return render_template("layout.html", text = "هناك خطأ ما")
            
            try: 
                witcher_data = req.json()
            except:
                return render_template("layout.html", text = "هناك خطأ ما")

            dates = []
            values = []
            desc = []
            icons = []

            for date in witcher_data["list"]:
                dates.append(date["dt_txt"])
                
            wanted = "12:00:00"

            result = list(filter(lambda x: wanted in x, dates))

            for date in witcher_data["list"]:
                if date["dt_txt"] in result:
                    values.append(date["main"]["temp"])
                    desc.append(date["weather"][0]["description"])
                    icon = date["weather"][0]["icon"]
                    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
                    icons.append(icon_url)

            weather = {
                "temperature": values, 
                "description" : desc, 
                "icon" : icons, 
                "cityname" : name
            }

            # print(witcher_data)
            # print(temp, desc, name)
            return render_template("layout.html", weather=weather)
    else:
        ...

if __name__ == "__main__":
    app.run(debug=True)