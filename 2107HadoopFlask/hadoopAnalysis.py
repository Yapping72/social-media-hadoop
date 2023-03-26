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
from io import BytesIO
import base64
import random



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
  
    #populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Energy.json") as f:
        data = json.load(f)
    

    with open("../data/Company Information/Company_Information.json", encoding='utf-8') as d:
        coydata = json.load(d)
        print(coydata['PepsiCo'])
    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Energy"]["word_count_dictionary"]

    #----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Energy"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))
    
   
    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    #----------used for plotting the word cloud---------------------------------



    #---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph 
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list 
    
    for key, value in word_freq.items():
        word_count_list.append((key, value))
    #---#this is used for plotting the bar graph for word count ----------------------------------

    #---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Energy':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
     #---#this is used for plotting the bar graph for one- five star review----------------------------------

  # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i<len(coyinfo):
        if coyinfo[i] in companies:
            data[coyinfo[i]]['information'] = coydata[coyinfo[i]]['employer_description']
            data[coyinfo[i]]['contact'] = coydata[coyinfo[i]]['website']
            data[coyinfo[i]]['founded'] = coydata[coyinfo[i]]['founded']
            data[coyinfo[i]]['hq'] = coydata[coyinfo[i]]['headquarters']
            data[coyinfo[i]]['size'] = coydata[coyinfo[i]]['size']
            data[coyinfo[i]]['type'] = coydata[coyinfo[i]]['type']
            data[coyinfo[i]]['industry'] = coydata[coyinfo[i]]['industry']
            data[coyinfo[i]]['revenue'] = coydata[coyinfo[i]]['revenue']
            data[coyinfo[i]]['mission'] = coydata[coyinfo[i]]['mission']

        i = i + 1;


    return render_template("EnergyPage.html", companies= companies, data=data,  image_data=img_data, word_count_list = word_count_list, 
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,
                      
                           )





@app.route("/")
def index():
    # Load the JSON data
    with open('../hadoop_analysis/Results/Energy.json') as f:
        Energydata = json.load(f)

    medianreviews = Energydata["Energy"]["median_reviews"]

    totalreviews = Energydata["Energy"]["total_reviews"]

    onestarreview = Energydata["Energy"]["one_star_reviews"]
    
    twostarreview = Energydata["Energy"]["two_star_reviews"]
    
    threestarreview = Energydata["Energy"]["three_star_reviews"]
    
    fourstarreview = Energydata["Energy"]["four_star_reviews"]
    
    fivestarreview = Energydata["Energy"]["five_star_reviews"]
  



    return render_template("index.html", totalreviews = totalreviews, totalmedianreviews = medianreviews, totalonestar = onestarreview, totaltwostar = twostarreview ,
                            totalthreestar = threestarreview, totalfourstar =fourstarreview, totalfivestar = fivestarreview
                            )


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




