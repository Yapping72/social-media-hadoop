import os
import sys
from flask import Flask,render_template, url_for,redirect, session, request
from flask import request,jsonify
from datetime import timedelta
import datetime
import json
import os
from collections import Counter
from wordcloud import WordCloud

app = Flask(__name__)




# displays fifth page
@app.route("/fifthpage")
def fifthpage():
   
    return render_template("fifthpage.html"
                         
                           )


#displays fourth page
@app.route("/fourthpage")
def fourthpage():
 
    return render_template("fourthpage.html")


#displays third page
@app.route("/thirdpage")

def thirdpage():
   

   return render_template("thirdpage.html" )




@app.route("/energypage")
def energypage():
  
    
    with open("../hadoop_analysis/Results/Energy.json") as f:
        data = json.load(f)

    print(data)
    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    return render_template("EnergyPage.html", companies= companies, data=data)





# function to generate word cloud
def generate_wordcloud(words):
    wc = WordCloud(width=800, height=400, max_words=50, background_color='white').generate_from_frequencies(words)
    return wc.to_image()




@app.route("/")
def index():
    # Load the JSON data
    with open('../hadoop_analysis/Results/Energy.json') as f:
        Energydata = json.load(f)

    
    # Loop over all the companies in the data and accumulate the data in json file
    total_two_star_reviews = 0
    total_energy_reviews= 0
    total_median_reviews= 0
    total_five_star_reviews= 0
    total_four_star_reviews= 0
    total_three_star_reviews= 0
    total_one_star_reviews= 0
    total_percent_five_star= 0
    total_percent_four_star =0
    total_percent_three_star =0 
    total_percent_two_star = 0
    total_percent_one_star =0

    for name, company_data in Energydata.items():
        #total reviews for energy sector
        total_energy_reviews += company_data['total_reviews']
        #total median reviews
        total_median_reviews += company_data['median_reviews']
        #total star reviews
        total_two_star_reviews += company_data['two_star_reviews']
        total_five_star_reviews += company_data['five_star_reviews']
        total_four_star_reviews += company_data['four_star_reviews']
        total_three_star_reviews += company_data['three_star_reviews']
        total_one_star_reviews += company_data['one_star_reviews']
        #percentage of fivestar-one star reviews
        total_percent_five_star += company_data['percent_five_star']
        total_percent_four_star += company_data['percent_four_star']
        total_percent_three_star += company_data['percent_three_star']
        total_percent_two_star += company_data['percent_two_star']
        total_percent_one_star += company_data['percent_one_star']



    return render_template("index.html", totalreviews = total_energy_reviews, totalmedianreviews = total_median_reviews, totalonestar = total_one_star_reviews, totaltwostar = total_two_star_reviews ,
                            totalthreestar = total_three_star_reviews, totalfourstar =total_four_star_reviews, totalfivestar = total_five_star_reviews
                            )


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




