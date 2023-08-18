// Made by Justin Herzog March 27th 2023
// api key dvpXhJhzPtMuUNiHu6Th

let PRICE_PER_TROY_OUNCE;

function getGoldPrice() {
    // The api gives us the price in USD per Troy Ounce
    API_URL = `https://data.nasdaq.com/api/v3/datasets/LBMA/GOLD?limit=1&column_index=1&api_key=dvpXhJhzPtMuUNiHu6Th`;
    console.log(API_URL);


    fetch(API_URL)
    .then(response => {
        return response.json();
    })
    .then(json => {
        theData = json.dataset.data[0];
        console.log(theData);
        resultMessage = `The Most Recent Price of Gold Provided Is From ${theData[0]}. This Price Is \$${theData[1]} Per Troy Ounce.`;
        PRICE_PER_TROY_OUNCE = theData[1];
        document.querySelector("#api-paragraph").innerHTML = resultMessage;
    })
    .catch(err => {
        let message = `Failed to recieve any data from the api for this reason: ${err}`;
        console.log(err);
        document.querySelector("#api-paragraph").innerHTML = message;
    })
    .finally(() => {
        console.log("All done!");
        
    });


}

function calculate(weight, unit) {

    // Performs a Get Request to our API in unitconv and add a div to the screen with the results
    let div = document.createElement("div");
    div.setAttribute("class", "green stuff-box");
    div.addEventListener("click", () => {
        div.remove();
    });

    // Checks to see if the user did anything sneaky...
    if (weight.length === 0) {
        div.setAttribute("class", "red stuff-box");
        div.innerHTML = "ERROR: You must have forgot to enter a weight. Try again.";
        document.getElementById('results').prepend(div);
        return;

    }
    else if (isNaN(parseFloat(weight)) || weight.includes("e")) {
        div.setAttribute("class", "red stuff-box");
        div.innerHTML = "ERROR: You have managed to put in a weight that is not a number... Very icky, no good!";
        document.getElementById('results').prepend(div);
        return;       
        
    }
    else if (parseFloat(weight) < 0) {
        div.setAttribute("class", "red stuff-box");
        div.innerHTML = "ERROR: You cannot enter a negative weight (it doesn't even make sense). Try again.";
        document.getElementById('results').prepend(div);
        return;
  
    }
    // Check the unit conversion too
    else if (!["lb", "oz", "t_oz", "kg", "g", "T"].includes(unit)) {
        div.setAttribute("class", "red stuff-box");
        div.innerHTML = "ERROR: You tried to convert to a unit that is invalid... Very icky, no good!";
        document.getElementById('results').prepend(div);
        return;
    }

    // Perform a Get Request to our API that converts all the units and does some math.
    let convURL = `http://${location.host}/unitconv/convert?from=${unit}&to=t_oz&value=${weight}`;

    fetch(convURL)
    .then(response => {
        return response.json();
    })
    .then(json => {
        theData = json;
        let currentDate = new Date().toLocaleString();
        let troy_ounce_value = json.value;
        let value = json.value * PRICE_PER_TROY_OUNCE; 

        div.innerHTML = `At ${currentDate} ${weight} ${unit} Of Gold Is Worth \$${value}`;
        document.getElementById('results').prepend(div);
        return;
    })
    .catch(err => {
        message = `Failed to receive information on conversions factors for this reason ${err}`;
        console.log(message);
        div.innerHTML = message;
        document.getElementById('results').prepend(div);
        return;
    })
    .finally(() => {
        console.log("Done with conversion factor api");
    });

}

document.getElementById("calculate-button").addEventListener("click", () => {

    const weight = document.getElementById("weightfield").value;
    const unit = document.getElementById("unit").value;

    calculate(weight, unit);
    return;

});

getGoldPrice();
