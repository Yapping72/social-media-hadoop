document.addEventListener('DOMContentLoaded', () => {
    var companyDiv = document.getElementById('company-div')
    var companyDropdown = document.getElementById('company-dropdown')
    var options = companyDropdown.options;
    var onestarReviews = document.getElementById('1-star')
    var twostarReviews = document.getElementById('2-star')
    var threestarReviews = document.getElementById('3-star')
    var fourstarReviews = document.getElementById('4-star')
    var fivestarReviews = document.getElementById('5-star')
    var title = document.getElementById('div-title')
    var informationDiv = document.getElementById('div-coy')
    var companyName = document.getElementById('company-name')
    var companyContact = document.getElementById('company-contact')
    var companyDesc = document.getElementById('company-description')
    var companyFounded = document.getElementById('company-founded')
    var companyHQ = document.getElementById('company-headquarters')
    var companySize = document.getElementById('company-size')
    var companyType = document.getElementById('company-type')
    var companyIndustry = document.getElementById('company-industry')
    var companyRevenue = document.getElementById('company-revenue')
    var companyMission = document.getElementById('company-mission')

    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart;

    function populate(data){
        console.log(data)
        for (let i = 0; i < options.length; i++) {
            options[i].setAttribute('data-one', data[options[i].value]["one_star_reviews"])
            options[i].setAttribute('data-two', data[options[i].value]["two_star_reviews"])
            options[i].setAttribute('data-three', data[options[i].value]["three_star_reviews"])
            options[i].setAttribute('data-four', data[options[i].value]["four_star_reviews"])
            options[i].setAttribute('data-five', data[options[i].value]["five_star_reviews"])
            options[i].setAttribute('data-percentone', data[options[i].value]["percent_one_star"])
            options[i].setAttribute('data-percenttwo', data[options[i].value]["percent_two_star"])
            options[i].setAttribute('data-percentthree', data[options[i].value]["percent_three_star"])
            options[i].setAttribute('data-percentfour', data[options[i].value]["percent_four_star"])
            options[i].setAttribute('data-percentfive', data[options[i].value]["percent_five_star"])

        }
    }
    
    populate(data)
    companyDropdown.addEventListener('change', (event) => {
      var selectedOption = companyDropdown.selectedIndex
      var dataset = options[selectedOption].dataset
      companyDiv.style.display = 'block';
      onestarReviews.innerText = dataset['one']
      twostarReviews.innerText = dataset['two']
      threestarReviews.innerText = dataset['three']
      fourstarReviews.innerText = dataset['four']
      fivestarReviews.innerText = dataset['five']
      if(event.target.value == options[0].value){
          informationDiv.style.display = 'none';
          console.log("YAPPING BLACK COCK")
      }else{
          informationDiv.style.display = 'block';
          companyName.innerText = "Name: "+data[event.target.value]['name']
          companyContact.innerText = "Website: "+data[event.target.value]['contact']
          companyDesc.innerText = "Description: "+data[event.target.value]['information']
          companyFounded.innerText = "Founded: "+data[event.target.value]['founded']
          companyHQ.innerText = "Headquarters: " +data[event.target.value]['hq']
          companySize.innerText = "Size: "+data[event.target.value]['size']
          companyType.innerText = "Type "+data[event.target.value]['type']
          companyIndustry.innerText = "Industry: "+data[event.target.value]['industry']
          companyRevenue.innerText = "Revenue: "+data[event.target.value]['revenue']
          companyMission.innerText = "Mission: " +data[event.target.value]['mission']
      }



      title.innerText = "Total Star Reviews for " + event.target.value
      // Destroy the old chart
      if(myChart){
        myChart.destroy();
      }
      myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ["1 Star reviews", "2 Star reviews", "3 Star reviews", "4 Star reviews","5 Star reviews "],
          datasets: [{
            backgroundColor: [
              "#2ecc71",
              "#3498db",
              "#95a5a6",
              "#9b59b6",
              "#f1c40f",
              "#e74c3c",
              "#34495e"
            ],
               data: [
               dataset['percentone'],
               dataset['percenttwo'],
               dataset['percentthree'],
               dataset['percentfour'],
               dataset['percentfive']
            ]
          }]
        }
      });
    });
});

