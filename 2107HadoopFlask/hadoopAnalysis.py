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


#displays second page
@app.route("/secondpage")

def secondpage():
   #populate companies to dropdown list.
    with open("./hadoop_analysis/Results/Communication Services.json") as f:
        commsdata = json.load(f)

    #populate companies to dropdown list.
    with open("./hadoop_analysis/Results/Financials.json") as f:
        financedata = json.load(f)

    commsmedianreviews = commsdata["Communication Services"]["median_reviews"]
    commstotalreviews = commsdata["Communication Services"]["total_reviews"]
    commsonestarreview = commsdata["Communication Services"]["one_star_reviews"]
    commstwostarreview = commsdata["Communication Services"]["two_star_reviews"]
    commsthreestarreview = commsdata["Communication Services"]["three_star_reviews"]
    commsfourstarreview = commsdata["Communication Services"]["four_star_reviews"]
    commsfivestarreview = commsdata["Communication Services"]["five_star_reviews"]

    financemedianreviews = financedata["Financials"]["median_reviews"]
    financetotalreviews = financedata["Financials"]["total_reviews"]
    financeonestarreview = financedata["Financials"]["one_star_reviews"]
    financetwostarreview = financedata["Financials"]["two_star_reviews"]
    financethreestarreview = financedata["Financials"]["three_star_reviews"]
    financefourstarreview = financedata["Financials"]["four_star_reviews"]
    financefivestarreview = financedata["Financials"]["five_star_reviews"]

 


    return render_template("secondpage.html", commsmedianreviews = commsmedianreviews,
    commstotalreviews=commstotalreviews,
    commsonestarreview =commsonestarreview, 
    commstwostarreview =  commstwostarreview,
    commsthreestarreview = commsthreestarreview,
    commsfourstarreview =  commsfourstarreview, 
    commsfivestarreview = commsfivestarreview,

    financemedianreviews =  financemedianreviews,
    financetotalreviews =  financetotalreviews,
    financeonestarreview =  financeonestarreview,
    financetwostarreview = financetwostarreview,
    financethreestarreview =  financethreestarreview,
    financefourstarreview = financefourstarreview,
    financefivestarreview =  financefivestarreview
        )




@app.route("/energypage")
def energypage():

    #populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Energy.json") as f:
        data = json.load(f)
    


    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)



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


@app.route("/airlinespage")
def airlinespage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Airlines.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Airlines"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Airlines"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Airlines':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("AirlinesPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )

@app.route("/communicationservicespage")
def communicationservicespage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Communication Services.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Communication Services"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Communication Services"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Communication Services':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("CommunicationsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )

@app.route("/financialspage")
def financialsPage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Financials.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Financials"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Financials"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Financials':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("FinancialsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )

@app.route("/healthcarepage")
def healthcarepage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Healthcare.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Healthcare"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Healthcare"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Healthcare':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("HealthcarePage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )


@app.route("/industrialspage")
def industrialspage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Industrials.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Industrials"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Industrials"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Industrials':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("IndustrialsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )

@app.route("/informationtechnologypage")
def informationtechnologypage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Information Technology.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Information Technology"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Information Technology"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Information Technology':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("ITPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )


@app.route("/institutionspage")
def institutionspage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Institutions.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Institutions"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Institutions"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Institutions':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("InstitutionsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )

@app.route("/materialspage")
def materialspage():
    # populate companies to dropdown list.
    with open("../hadoop_analysis/Results/Materials.json") as f:
        data = json.load(f)

    with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
        coydata = json.load(d)
        print(coydata)

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Materials"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Materials"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Materials':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    while i < len(coyinfo):
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

    return render_template("MaterialsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )
############################################################
# Uncomment this Segment when consumer discretionary is done#
############################################################
# @app.route("/consumerdiscretionarypage")
# def consumerdiscretionarypage():
#     # populate companies to dropdown list.
#     with open("../hadoop_analysis/Results/Consumer Discretionary.json") as f:
#         data = json.load(f)
#
#     with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
#         coydata = json.load(d)
#         print(coydata)
#
#     companies = []
#     for key in data:
#         company_name = data[key]['name']
#         companies.append(company_name)
#
#     # Extract word frequencies
#     word_freq = data["Consumer Discretionary"]["word_count_dictionary"]
#
#     # ----------used for plotting the word cloud---------------------------------
#     # Sort word frequencies by count and take top 5
#     top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
#
#     # Sort top words by value in the JSON
#     top_words = sorted(top_words, key=lambda x: data["Consumer Discretionary"]["word_count_dictionary"][x[0]], reverse=True)
#
#     # Generate word cloud image
#     wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))
#
#     # Get the image as bytes and encode it as base64
#     img_bytes = BytesIO()
#     wordcloud.to_image().save(img_bytes, format='PNG')
#     img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
#     # ----------used for plotting the word cloud---------------------------------
#
#     # ---#this is used for plotting the bar graph for word count----------------------------------
#     # Create an empty list to store the key-value pairs this is used for plotting the bar graph
#     word_count_list = []
#     # Iterate through the dictionary and append the key-value pairs to the list
#
#     for key, value in word_freq.items():
#         word_count_list.append((key, value))
#     # ---#this is used for plotting the bar graph for word count ----------------------------------
#
#     # ---#this is used for plotting the bar graph for one - five star review----------------------------------
#     # initialize empty list to store one-star reviews
#     one_star_reviews = []
#     two_star_reviews = []
#     three_star_reviews = []
#     four_star_reviews = []
#     five_star_reviews = []
#
#     # iterate through each company's data, excluding Energy
#     for company, company_data in data.items():
#         if company != 'Consumer Discretionary':
#             one_star_reviews.append((company, company_data['one_star_reviews']))
#             two_star_reviews.append((company, company_data['two_star_reviews']))
#             three_star_reviews.append((company, company_data['three_star_reviews']))
#             four_star_reviews.append((company, company_data['four_star_reviews']))
#             five_star_reviews.append((company, company_data['five_star_reviews']))
#     # ---#this is used for plotting the bar graph for one- five star review----------------------------------
#
#     # Extract the company names from the JSON data and store them in a list
#     coyinfo = [coy for coy in coydata.keys()]
#     i = 0;
#     while i < len(coyinfo):
#         if coyinfo[i] in companies:
#             data[coyinfo[i]]['information'] = coydata[coyinfo[i]]['employer_description']
#             data[coyinfo[i]]['contact'] = coydata[coyinfo[i]]['website']
#             data[coyinfo[i]]['founded'] = coydata[coyinfo[i]]['founded']
#             data[coyinfo[i]]['hq'] = coydata[coyinfo[i]]['headquarters']
#             data[coyinfo[i]]['size'] = coydata[coyinfo[i]]['size']
#             data[coyinfo[i]]['type'] = coydata[coyinfo[i]]['type']
#             data[coyinfo[i]]['industry'] = coydata[coyinfo[i]]['industry']
#             data[coyinfo[i]]['revenue'] = coydata[coyinfo[i]]['revenue']
#             data[coyinfo[i]]['mission'] = coydata[coyinfo[i]]['mission']
#
#         i = i + 1;
#
#     return render_template("ConsumerDiscretionaryPage.html", companies=companies, data=data, image_data=img_data,
#                            word_count_list=word_count_list,
#                            one_star_reviews=one_star_reviews,
#                            two_star_reviews=two_star_reviews,
#                            three_star_reviews=three_star_reviews,
#                            four_star_reviews=four_star_reviews,
#                            five_star_reviews=five_star_reviews,
#
#                            )


#######################################################
# Uncomment this Segment when consumer staples is done#
#######################################################
# @app.route("/consumerstaplespage")
# def consumerstaplespage():
#     # populate companies to dropdown list.
#     with open("../hadoop_analysis/Results/Consumer Staples.json") as f:
#         data = json.load(f)
#
#     with open("../data/Company Information/Company_Information.json", encoding="utf-8") as d:
#         coydata = json.load(d)
#         print(coydata)
#
#     companies = []
#     for key in data:
#         company_name = data[key]['name']
#         companies.append(company_name)
#
#     # Extract word frequencies
#     word_freq = data["Consumer Staples"]["word_count_dictionary"]
#
#     # ----------used for plotting the word cloud---------------------------------
#     # Sort word frequencies by count and take top 5
#     top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
#
#     # Sort top words by value in the JSON
#     top_words = sorted(top_words, key=lambda x: data["Consumer Staples"]["word_count_dictionary"][x[0]], reverse=True)
#
#     # Generate word cloud image
#     wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))
#
#     # Get the image as bytes and encode it as base64
#     img_bytes = BytesIO()
#     wordcloud.to_image().save(img_bytes, format='PNG')
#     img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
#     # ----------used for plotting the word cloud---------------------------------
#
#     # ---#this is used for plotting the bar graph for word count----------------------------------
#     # Create an empty list to store the key-value pairs this is used for plotting the bar graph
#     word_count_list = []
#     # Iterate through the dictionary and append the key-value pairs to the list
#
#     for key, value in word_freq.items():
#         word_count_list.append((key, value))
#     # ---#this is used for plotting the bar graph for word count ----------------------------------
#
#     # ---#this is used for plotting the bar graph for one - five star review----------------------------------
#     # initialize empty list to store one-star reviews
#     one_star_reviews = []
#     two_star_reviews = []
#     three_star_reviews = []
#     four_star_reviews = []
#     five_star_reviews = []
#
#     # iterate through each company's data, excluding Energy
#     for company, company_data in data.items():
#         if company != 'Consumer Staples':
#             one_star_reviews.append((company, company_data['one_star_reviews']))
#             two_star_reviews.append((company, company_data['two_star_reviews']))
#             three_star_reviews.append((company, company_data['three_star_reviews']))
#             four_star_reviews.append((company, company_data['four_star_reviews']))
#             five_star_reviews.append((company, company_data['five_star_reviews']))
#     # ---#this is used for plotting the bar graph for one- five star review----------------------------------
#
#     # Extract the company names from the JSON data and store them in a list
#     coyinfo = [coy for coy in coydata.keys()]
#     i = 0;
#     while i < len(coyinfo):
#         if coyinfo[i] in companies:
#             data[coyinfo[i]]['information'] = coydata[coyinfo[i]]['employer_description']
#             data[coyinfo[i]]['contact'] = coydata[coyinfo[i]]['website']
#             data[coyinfo[i]]['founded'] = coydata[coyinfo[i]]['founded']
#             data[coyinfo[i]]['hq'] = coydata[coyinfo[i]]['headquarters']
#             data[coyinfo[i]]['size'] = coydata[coyinfo[i]]['size']
#             data[coyinfo[i]]['type'] = coydata[coyinfo[i]]['type']
#             data[coyinfo[i]]['industry'] = coydata[coyinfo[i]]['industry']
#             data[coyinfo[i]]['revenue'] = coydata[coyinfo[i]]['revenue']
#             data[coyinfo[i]]['mission'] = coydata[coyinfo[i]]['mission']
#
#         i = i + 1;
#
#     return render_template("ConsumerStaplesPage.html", companies=companies, data=data, image_data=img_data,
#                            word_count_list=word_count_list,
#                            one_star_reviews=one_star_reviews,
#                            two_star_reviews=two_star_reviews,
#                            three_star_reviews=three_star_reviews,
#                            four_star_reviews=four_star_reviews,
#                            five_star_reviews=five_star_reviews,
#
#                            )

@app.route("/")
def index():
    # Load the JSON data
    with open('../hadoop_analysis/Results/Energy.json') as f:
        Energydata = json.load(f)
    with open('../hadoop_analysis/Results/Airlines.json') as f:
        Airlinesdata = json.load(f)

    medianreviews = Energydata["Energy"]["median_reviews"]
    totalreviews = Energydata["Energy"]["total_reviews"]
    onestarreview = Energydata["Energy"]["one_star_reviews"]
    twostarreview = Energydata["Energy"]["two_star_reviews"]
    threestarreview = Energydata["Energy"]["three_star_reviews"]
    fourstarreview = Energydata["Energy"]["four_star_reviews"]
    fivestarreview = Energydata["Energy"]["five_star_reviews"]
  
    airlinemedianreviews = Airlinesdata["Airlines"]["median_reviews"]
    airlinetotalreviews = Airlinesdata["Airlines"]["total_reviews"]
    airlineonestarreview = Airlinesdata["Airlines"]["one_star_reviews"]
    airlinetwostarreview = Airlinesdata["Airlines"]["two_star_reviews"]
    airlinethreestarreview = Airlinesdata["Airlines"]["three_star_reviews"]
    airlinefourstarreview = Airlinesdata["Airlines"]["four_star_reviews"]
    airlinefivestarreview = Airlinesdata["Airlines"]["five_star_reviews"]

                          


    return render_template("index.html", totalreviews = totalreviews, totalmedianreviews = medianreviews, totalonestar = onestarreview, totaltwostar = twostarreview ,
                            totalthreestar = threestarreview, totalfourstar =fourstarreview, totalfivestar = fivestarreview,
                            airlinemedianreviews =  airlinemedianreviews,
                            airlinetotalreviews = airlinetotalreviews,
                            airlineonestarreview = airlineonestarreview,
                            airlinetwostarreview  = airlinetwostarreview,
                            airlinethreestarreview =airlinethreestarreview, 
                            airlinefourstarreview =  airlinefourstarreview,
                            airlinefivestarreview =airlinefivestarreview 




                            )


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




