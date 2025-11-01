import sys
import datetime
from googletrans import Translator
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton,QStackedWidget,QGridLayout
from PyQt5.QtCore import Qt
import requests

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.page_detail_button = QPushButton("Detalis",)
        self.cache = {}
        self.translator = Translator()
        self.current_lang = "en"
        self.page_lang_box = QComboBox()
        self.page_lang_box.addItems(["English", "Türkçe"])
        self.page_humidity_pressure = QLabel()
        self.page_status_day = QLabel()
        self.page_wind_label = QLabel()
        self.setGeometry(800,250,400,450)
        self.page_city_name_label = QLabel()
        self.setWindowTitle("🌦️ Weather App 🌦️")
        self.page_city_label = QLabel("Enter a city",)
        self.page_forecast_label = QLabel()
        self.page_input_city = QLineEdit()
        self.page_input_city.setPlaceholderText("Enter a city: ")
        self.page_temperature_label = QLabel()
        self.page_emoji_label = QLabel()
        self.page_description_label = QLabel()
        self.detail_back_button = QPushButton("Home Page")


        self.forecast_data = {}
        self.data = {}

        page_home = self.home_page()
        page_detail = self.detail_page()

        self.stack = QStackedWidget()
        self.stack.addWidget(page_home)
        self.stack.addWidget(page_detail)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)
        self.show_main_page()
        self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #c9d6ff, stop:1 #e2e2e2
                    );
                    font-family: "Segoe UI";
                    color: #333;
                }
                """)

    def home_page(self):
        page_home_widget = QWidget()
        page_home_layout = QVBoxLayout(page_home_widget)

        hbox = QHBoxLayout()
        hbox.addWidget(self.page_city_label)
        hbox.addWidget(self.page_lang_box)

        page_home_layout.addLayout(hbox)
        page_home_layout.addWidget(self.page_input_city)
        page_home_layout.addWidget(self.page_city_name_label)
        page_home_layout.addWidget(self.page_temperature_label)
        page_home_layout.addWidget(self.page_emoji_label)
        page_home_layout.addWidget(self.page_humidity_pressure)
        page_home_layout.addWidget(self.page_status_day)
        page_home_layout.addWidget(self.page_wind_label)
        page_home_layout.addWidget(self.page_description_label)
        page_home_layout.addWidget(self.page_forecast_label)
        page_home_layout.addWidget(self.page_detail_button)
        return page_home_widget

    def detail_page(self):
        page_detail_widget = QWidget()
        self.detail_city_name_label = QLabel()
        vbox = QVBoxLayout(page_detail_widget)


        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setAlignment(Qt.AlignCenter)
        # Sol başlıklar (6 satır)
        headers = ["Days", "Temp", "Humidity/Pressure", "Wind", "Emoji", "Description"]
        for row in range(len(headers)):
            h = QLabel(headers[row])
            h.setAlignment(Qt.AlignCenter)
            h.setStyleSheet("font-weight:bold; font-size:25px; border:1px solid #bbb; padding:20px;")
            self.grid.addWidget(h, row, 0)
        self.table_cells = {
            "day": [],
            "temp": [],
            "hum": [],
            "wind": [],
            "emoji": [],
            "desc": []
        }

        def make_cell():
            lbl = QLabel("-")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("border:3px solid #ddd; font-size:25px; padding:6px;")
            return lbl

        for col in range(1, 6):  # 1..5 sütunlar
            d = make_cell();self.grid.addWidget(d, 0, col);self.table_cells["day"].append(d)
            t = make_cell();self.grid.addWidget(t, 1, col);self.table_cells["temp"].append(t)
            h = make_cell();self.grid.addWidget(h, 2, col);self.table_cells["hum"].append(h)
            w = make_cell();self.grid.addWidget(w, 3, col);self.table_cells["wind"].append(w)
            e = make_cell();self.grid.addWidget(e, 4, col);self.table_cells["emoji"].append(e)
            s = make_cell();self.grid.addWidget(s, 5, col);self.table_cells["desc"].append(s)
        self.grid.addWidget(self.detail_back_button, 6, 0, 1, 6)
        for i in range(1,6):
            self.table_cells["day"][i-1].setStyleSheet("font-weight:bold; font-size:25px; border:1px solid #bbb; padding:20px;")
        vbox.addWidget(self.detail_city_name_label)
        vbox.addLayout(self.grid)
        self.detail_city_name_label.setAlignment(Qt.AlignCenter)
        self.detail_city_name_label.setStyleSheet("font-weight:bold; font-size:25px; border:1px solid #bbb; padding:20px;")

        return page_detail_widget

    def show_main_page(self):
        self.stack.setCurrentWidget(self.stack.widget(0))
        for widget, name in zip(
                [self.page_detail_button,self.page_humidity_pressure,self.page_status_day,self.page_wind_label,self.page_city_name_label,
                 self.page_city_label,self.page_input_city, self.page_temperature_label, self.page_emoji_label,
                 self.page_description_label,self.page_forecast_label],
                ["page_detail_button","page_humidity_pressure","page_status_day","page_wind_label","page_city_name_label","page_city_label","page_input_city",
                 "page_temperature_label", "page_emoji_label", "page_description_label","page_forecast_label"]):
            widget.setObjectName(name)
        for widget in [self.page_humidity_pressure,self.page_status_day,self.page_wind_label,self.page_city_name_label,self.page_city_label,
                       self.page_input_city, self.page_temperature_label, self.page_emoji_label, self.page_description_label,self.page_forecast_label]:
            widget.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
        QLineEdit#page_input_city {
                    font-size: 30px;
                    padding: 12px;
                    border: 2px solid #5b86e5;
                    border-radius: 15px;
                    background-color: #ffffff;
                    color: #333;
}
        QLineEdit#page_input_city:focus {
            border-color: #36d1dc;
            box-shadow: 0 0 10px #36d1dc;
        }
        
        QPushButton#page_detail_button {
            font-size: 26px;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px 20px;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #36d1dc, stop:1 #5b86e5);
        }
        QPushButton#page_detail_button:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #5b86e5, stop:1 #36d1dc);
        }
        
        QLabel#page_city_label {
            font-size: 45px;
            font-weight: bold;
            color: #004aad;
        }
        QLabel {
            font-size: 23px;
            font-weight: bold;
            color: #004aad;
        }
        
        QLabel#page_temperature_label {
            font-size: 28px;
            font-weight: bold;
            color: #222;
        }
        
        QLabel#page_emoji_label {
            font-size: 90px;
            color:None;
        }
        
        QLabel#page_description_label {
            font-size: 35px;
            color: #555;
        }

                           """)
        self.page_input_city.returnPressed.connect(self.button_click)
        self.page_lang_box.currentTextChanged.connect(self.change_language)
        self.page_detail_button.clicked.connect(self.show_detail_page)

    def show_detail_page(self):
        if not self.forecast_data:
            self.page_temperature_label.setText("There is no Data!")
            return
        self.stack.setCurrentWidget(self.stack.widget(1))

        self.detail_back_button.clicked.connect(self.show_main_page)
        self.detail_city_name_label.setObjectName("detail_city_name_label")
        self.setStyleSheet("""
        QLabel#detail_city_name_label {
            color: darkgreen;
            font-size: 45px;
            font-weight: bold;
            border-radius: 20px;
            border: 2px solid #5b86e5;
            border-color : lightgreen;
            padding: 15px;
            margin: 10px;
        }
        
        QLabel {
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            background-color: #fdfdfd;
        }
        QLabel:hover {
            background-color: #eef5ff;
            transition: 0.3s;
        }
        
        QPushButton {
            border-radius: 15px;
            padding: 10px 25px;
        }
        QPushButton:hover {
            background-color: #dce7ff;
        }  """)
        self.display_detail_info()
    def change_language(self,lang):
        if lang == "Türkçe":
            self.current_lang = "tr"
        else:
            self.current_lang = "en"
        if self.data:
            self.display_Info()
            if self.forecast_data:
                self.forecast_Info()
    def translate(self,text):
        if self.current_lang == "en":
            return text
        custom_dict = {
            "Feels Like": "Hissedilen",
            "Humidity": "Nem",
            "Pressure": "Basınç",
            "Wind Speed": "Rüzgar Hızı",
            "Wind Direction": "Rüzgar Yönü",
            "Sunrise": "Gün Doğumu",
            "Sunset": "Gün Batımı",
            "Clear Sky": "Açık Hava",
            "Few Clouds": "Az Bulutlu",
            "Scattered Clouds": "Dağınık Bulutlar",
            "Broken Clouds": "Parçalı Bulutlu",
            "Rain": "Yağmur",
            "Thunderstorm": "Gök Gürültülü Fırtına",
            "Snow": "Kar",
            "Mist": "Sis",
        }
        for key,value in custom_dict.items():
            if self.current_lang == 'en':
                if key in text:
                    text = text.replace(key,value)
        if  text in self.cache:
            return self.cache[text]
        try:
            translated = self.translator.translate(text, src="en", dest=self.current_lang)
            self.cache[text] = translated.text
            return translated.text
        except :
            self.page_temperature_label.setText("Failed to translate")
            return text
    def button_click(self):
        api_key = "89a4ae276eb44170d36855e1b0b42aed"
        city = self.page_input_city.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=en"
        forecast_res=None
        response = None
        try:
            response = requests.get(url)
            response.raise_for_status()
            forecast_res = requests.get(forecast_url)
            forecast_res.raise_for_status()
            self.forecast_data = forecast_res.json()
            self.data = response.json()
            self.display_Info()
            self.forecast_Info()
        except Exception as e:
            if forecast_res is not None and hasattr(forecast_res ,"status_code") and forecast_res.status_code !=200:
                self.display_Eror(e,forecast_res)
            else:
                for label in [self.page_temperature_label,self.page_emoji_label,self.page_city_name_label,self.page_description_label,
                              self.page_humidity_pressure,self.page_wind_label,self.page_status_day,self.page_forecast_label]:
                    label.clear()
                self.display_Eror(e,response)
    def display_Eror(self,error,response):
        match error.__class__.__name__:
            case "ConnectionError":
                self.page_temperature_label.setText("Bağlantı hatası:")
                return
            case "Timeout":
                self.page_temperature_label.setText("Zaman aşımı hatası:")
                return
            case "RequestException":
                self.page_temperature_label.setText("İstek sırasında başka bir hata:")
                return
            case "ValueError":
                self.page_temperature_label.setText("JSON verisi çözümlenemedi:")
                return
            case "HTTPError":
                if response is None:
                    self.page_temperature_label.setText("⚠️ Sunucuya ulaşılamadı.")
                    return
                match response.status_code:
                    case 400:
                        self.page_temperature_label.setText(f"❌ Geçersiz istek. \n(Hata Kodu: {response.status_code})")
                    case 401:
                        self.page_temperature_label.setText(f"🔐 Yetkilendirme hatası! API anahtarın geçersiz olabilir. \n(Hata Kodu: {response.status_code})")
                    case 403:
                        self.page_temperature_label.setText(f"🚫 Erişim yasak. Sunucu isteğini reddetti. \n(Hata Kodu: {response.status_code})")
                    case 404:
                        self.page_temperature_label.setText(f"🌆 Şehir veya sayfa bulunamadı. \n(Hata Kodu. {response.status_code})")
                    case 429:
                        self.page_temperature_label.setText(f"⚠️ Çok fazla istek gönderdin! Lütfen biraz bekle. \n(Hata Kodu: {response.status_code})")
                    case 500:
                        self.page_temperature_label.setText(f"💥 Sunucu hatası. Sorun bizde! \n(Hata Kodu: {response.status_code})")
                    case 502:
                        self.page_temperature_label.setText(f"🔧 Geçersiz yanıt. Sunucu arka planda düzgün çalışmıyor. \n(Hata Kodu: {response.status_code})")
                    case 503:
                        self.page_temperature_label.setText(
                            f"🕒 Sunucu geçici olarak hizmet dışı. Lütfen sonra tekrar dene. \n(Hata Kodu: {response.status_code})")
                    case 504:
                        self.page_temperature_label.setText(
                            f"⏳ Sunucu zaman aşımına uğradı. Bağlantı çok yavaş olabilir. \n(Hata Kodu: {response.status_code})")
                    case _:
                        self.page_temperature_label.setText(f"❓ Beklenmeyen bir hata oluştu. \n(Hata Kodu: {response.status_code})")

    def display_Info(self):
            timezone_offset = self.data['timezone']
            sunrise = datetime.datetime.utcfromtimestamp(self.data['sys']['sunrise']+timezone_offset)
            sunset =  datetime.datetime.utcfromtimestamp(self.data['sys']['sunset']+timezone_offset)
            now = datetime.datetime.utcfromtimestamp(datetime.datetime.utcnow().timestamp()+timezone_offset)
            humidity = self.data['main']['humidity']
            pressure = self.data['main']['pressure']
            if sunrise <= now <= sunset:
                day_status = "🌞 Noon"
            else:
                day_status = "🌙 Night"
            self.page_humidity_pressure.setText(self.translate(f"💧Humidity: %{humidity}   ⚙️Pressure:{pressure}hpa"))
            self.page_status_day.setText(self.translate(f"{day_status}\n🌅 Sunrise: {sunrise.strftime('%H:%M:%S')}\n🌇 Sunset: {sunset.strftime('%H:%M:%S')}"))
            name = self.data["name"]
            wind_speed = self.data['wind']['speed'] *3.6
            wind_deg = self.data['wind']['deg']
            directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
            wind_dir = directions[int((wind_deg + 22.5) // 45) % 8]
            country_name = self.data["sys"]["country"]
            temperature = self.data['main']['temp'] -273.15
            feeling_temperature = self.data['main']['feels_like'] -273.15
            description =self.data['weather'][0]['description']
            weatherId = self.data['weather'][0]['id']
            emogy= self.display_emoji(weatherId)
            self.page_city_name_label.setText(self.translate(f"{name.capitalize()} / {country_name.capitalize()}"))
            self.page_temperature_label.setText(self.translate(f"{temperature:.2f}°C(Feels Like: {feeling_temperature:.2f}°C)"))
            self.page_description_label.setText(self.translate(f"{description.capitalize()}"))
            self.page_emoji_label.setText(emogy)
            self.page_wind_label.setText(self.translate(f"Wind Speed: {wind_speed:.2f}km/h\nWind Direction: {wind_dir}"))


    def display_detail_info(self):
        days_added = 0
        for contant in self.forecast_data['list']:
            date = contant['dt_txt'].split(" ")[0]
            time = contant['dt_txt'].split(" ")[1]
            days = datetime.datetime.strptime(date, "%Y-%m-%d")
            day = days.strftime("%A")
            name = self.forecast_data['city']['name']
            country_name = self.forecast_data['city']['country']
            self.detail_city_name_label.setText(f"{name} / {country_name}")
            if "12:00:00" in time:
                weatherId = contant['weather'][0]['id']
                emogy = MainWindow.display_emoji(weatherId)
                temp = contant["main"]["temp"]
                desc = contant['weather'][0]['description']
                humidity = contant['main']['humidity']
                pressure = contant['main']['pressure']
                wind_speed = contant['wind']['speed'] * 3.6
                wind_deg = contant['wind']['deg']
                directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
                wind_dir = directions[int((wind_deg + 22.5) // 45) % 8]
                feeling_temperature = contant['main']['feels_like']
                #Yazdırma--------------------------------
                self.table_cells["day"][days_added].setText(f"{day}")
                self.table_cells["temp"][days_added].setText(f"{temp}C°\n({feeling_temperature})")
                self.table_cells["hum"][days_added].setText(f"%{humidity}\n{pressure}hpa")
                self.table_cells["wind"][days_added].setText(f"{wind_speed:.2f}\n{wind_dir}")
                self.table_cells["emoji"][days_added].setText(f"{emogy}")
                self.table_cells["desc"][days_added].setText(f"{desc}")
                days_added += 1
            if days_added == 5:
                break
    def forecast_Info(self):
        days_added = 0
        text = ""
        for contant in self.forecast_data['list']:
            date = contant['dt_txt'].split(" ")[0]
            time = contant['dt_txt'].split(" ")[1]
            days = datetime.datetime.strptime(date,"%Y-%m-%d")
            day = days.strftime("%A")
            if "12:00:00" in time:
                weatherId = contant['weather'][0]['id']
                emogy = self.display_emoji(weatherId)
                temp = contant["main"]["temp"]
                desc = contant['weather'][0]['description']
                text += f"{emogy} {day.capitalize()}:{temp}°C  {desc.capitalize()}\n"
                days_added +=1
            if days_added ==2:
                break
        self.page_forecast_label.setText(self.translate(text))
    @staticmethod
    def display_emoji(weatherId):
        if 200<=weatherId<=232:
            return "⛈️"
        if 300<=weatherId<=321:
            return "🌦️"
        if 500<=weatherId<=531:
            return "🌧️"
        if 600<=weatherId<=622:
            return "❄️"
        if weatherId==731:
            return "🏖️"
        if 701 <= weatherId <= 741:
            return "🌫️"
        if weatherId ==762 :
            return "🌋"
        if weatherId ==771 :
            return "🍃"
        if weatherId ==781 :
            return "🌪️"
        if weatherId ==800 :
            return "☀️"
        if 801 <= weatherId <= 804:
            return "☁️"

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
main()