
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests, time, random
from flask_cors import CORS, cross_origin

app = Flask(__name__)


CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class my_db(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    sl_no = db.Column(db.Integer, primary_key=True)
  
    info = db.Column(db.String(100), nullable=True)
    dwnlinks = db.Column(db.String(500), nullable=True)
   

    # def __repr__(self) -> str:
    #     return f"{self.sl_no} - {self.info} - {self.dwnlinks}"


def scrapper_func():
  
    url = ["https://newspaperpdf.online/the-hindu-pdf-download.php",
            "https://newspaperpdf.online/download-financial-express.php",
            "https://newspaperpdf.online/download-indian-express.php",
            "https://newspaperpdf.online/download-dainik-jagran.php",
            "https://newspaperpdf.online/download-economic-times.php",
            "https://newspaperpdf.online/download-deccan-chronicle.php",
            "https://newspaperpdf.online/download-jansatta.php",
            "https://newspaperpdf.online/download-hindustan-times.php",
            "https://newspaperpdf.online/download-times-of-india.php"
          ]  
    
    
    headers = [{ 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36' },
                             { 'User-Agent' :'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'},
                             { 'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'},
                             { 'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'},
                             { 'User-Agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'},
                             { 'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'} ]   
                
    
    lst = []    
    for i in range(len(url)):
        rand_heads = random.randint(0,5) 
        time.sleep(random.randint(5,15))
        res = requests.get(url[i], headers = headers[rand_heads])
        print(url[i])
        if res.status_code == 200 :
                print(res)
                soup = BeautifulSoup(res.text,'html.parser')
                all_links = soup.select("#containerid a")
                        # print(type(all_links))
               
                for link in all_links:
                        link_dict = {}
                        

                        dt_name = link.text 
                        link_dict['dt_name'] = dt_name
                        
                        links = link.get('href') 
                        link_dict['links'] = links         
                        lst.append(link_dict)
                # dt_lst.append(dt_name)
                
        else:
            print("website down") 
        time.sleep(random.randint(5,15))      
    # print(lst)
   
   #deleting for all records
    db.session.query(my_db).delete()
    db.session.commit()


    for i, item in enumerate(lst, 1):
   
        sl_no = i
        info = item['dt_name']
        dwnlinks = item['links']

        d_bse = my_db(sl_no=sl_no, info=info, dwnlinks=dwnlinks)
        db.session.add(d_bse)  #adding data to current session
        db.session.commit()
    print('Database has been successfully updated...')
    # return lst


    


sched = BackgroundScheduler(daemon=True)
sched.add_job(scrapper_func,'interval', minutes=30)
sched.start()


@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file():
     return "Downloaded :) !"

    
@app.route("/")
def home():
    """ Function for test purposes. """
    return "Welcome to API :) !"



@app.route("/api", methods = ['GET'])
@cross_origin()
def serving_api():
    
    if request.method == 'GET':
        all_db = []
        for i in range(1,64):
            db_dict = {}
            id_no = my_db.query.filter_by(sl_no=i).first()
            # print(type(id_no.info))
          
            db_dict['id'] = int(id_no.sl_no)
            db_dict['date'] = id_no.info
            db_dict['link'] = id_no.dwnlinks

            all_db.append(db_dict)
        return jsonify(data = all_db)


    

    
   


if __name__ == "__main__":
    app.run()
