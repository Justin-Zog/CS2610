// Abstract API URL to get the geolocation (latitude and longitude) of the users IP address
// Our api-key is: a724d87631014750a8eaa9b509e3d111
// https://ipgeolocation.abstractapi.com/v1/?api_key=a724d87631014750a8eaa9b509e3d111&fields=latitude,longitude

// Open Weather Map API URL to get the current weather conditions of the latitude and longitude fetched by Abstract API
// Our api-key is: 2a03caa6e6db72a3c442d86c79feab65
// https://api.openweathermap.org/data/2.5/weather?lat={{latitude}}&lon={{longitude}}&units=imperial&appid=2a03caa6e6db72a3c442d86c79feab65

// Forecast URL
// https://api.openweathermap.org/data/2.5/forecast?lat={{latitude}}&lon={{longitude}}&units=imperial&cnt=40&appid=2a03caa6e6db72a3c442d86c79feab65

const app = Vue.createApp({
    data() {
        return {
            'error': undefined,
            'location': undefined,
            'currentDay': new Date().toLocaleString(),
            'currentTemp': undefined,
            'maxTemp': undefined,
            'minTemp': undefined,
            'currentDescription': undefined,
            'currentHumidity': undefined,
            'currentPressure': undefined,
            'forecasts': undefined,
        };
    },

    created() {
        ABSTRACT_URL = "https://ipgeolocation.abstractapi.com/v1/?api_key=a724d87631014750a8eaa9b509e3d111&fields=latitude,longitude,city,region,country";

        const locationResult = fetch(ABSTRACT_URL)
        .then(response => {
            return response.json();
        })
        .then(json => {
            // Example Output
            //{"city":"Salt Lake City","region":"Utah","country":"United States","longitude":-111.8121,"latitude":40.627}
            if (json.latitude === undefined || json.longitude === undefined) {
                err = `You are probably making to many API requests by refreshing the page to quickly. Please try again to refresh the page, just once in about 30 seconds.`;
                throw err;
            }
            else {
                let city = undefined;
                let region = undefined;
                let country = undefined;
                if (json.city) city = json.city;
                if (json.region) region = json.region;
                if (json.country) country = json.country;
                let nonCoordinateText = [city, region, country].filter(Boolean).join(", ");
                this.location = `${nonCoordinateText} at coordinates (${json.latitude}, ${json.longitude})`;
            }

            fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${json.latitude}&lon=${json.longitude}&units=imperial&appid=2a03caa6e6db72a3c442d86c79feab65`)
            .then(response => {
                return response.json();
            })
            .then(json => {
                this.currentDescription = json.weather[0].description;
                main = json.main;
                this.currentTemp = main.temp;
                this.maxTemp = main.temp_max;
                this.minTemp = main.temp_min;
                this.currentPressure = main.pressure;
                this.currentHumidity = main.humidity;
    
            })
            .catch(err => {
                let message = `Failed to get the current weather from the API for this reason ${err}`;
                this.error = message;
            })
            .finally(() => {
                console.log("Finished current weather API call attempt.");
            });


            fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=${json.latitude}&lon=${json.longitude}&units=imperial&cnt=40&appid=2a03caa6e6db72a3c442d86c79feab65`)
            .then(response => {
                return response.json();
            })
            .then(json => {
                for (item of json.list) {
                    item.likeliness = 0;
                }
                this.forecasts = json.list;
            })
            .catch(err => {
                let message = `Failed to get the forecast info from the API for this reason ${err}`;
                this.error = message;
            })
            .finally(() => {
                console.log("Finished forecast API call attempt.")
            })

        })
        .catch(err => {
            let message = `Failed to retrieve location data from the API for this reason ${err}`;
            this.error = message;
            console.log(this.error);
        })
        .finally(() => {
            console.log("Finished location API call attempt.");
        });

        
    },

    methods: {
        toggle(event) {
            let idx = event.currentTarget.getAttribute('data-index');
            // 0 is neutral, 1 is likely, 2 is unlikely
            this.forecasts[idx].likeliness = ((this.forecasts[idx].likeliness + 1) % 3);
        },
    },

    computed: {
        vote() {
            let likely = 0;
            let unlikely = 0;
            let neutral = 0;
            for (let i in this.forecasts) {
                if (this.forecasts[i].likeliness === 0) {
                    neutral++;
                }
                else if (this.forecasts[i].likeliness === 1) {
                    likely++;
                }
                else {
                    unlikely++;
                }
            }
            return [neutral, likely, unlikely];
        },
    }
        
});

const vm = app.mount("#app");
