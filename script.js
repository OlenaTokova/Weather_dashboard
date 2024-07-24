document.getElementById('search-button').addEventListener('click', function() {
    const city = document.getElementById('city-input').value;
    const apiKey = 'c7b8df60ed4c438f0440190834ff99cf'; // Replace YOUR_API_KEY with your actual OpenWeather API key
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        const weatherOutput = `
            <h3>Weather in ${data.name}</h3>
            <p>Temperature: ${data.main.temp} °C</p>
            <p>Weather: ${data.weather[0].description}</p>
            <p>Humidity: ${data.main.humidity}%</p>
            <p>Wind Speed: ${data.wind.speed} m/s</p>
        `;
        document.getElementById('weather-details').innerHTML = weatherOutput;
    })
    .catch(error => console.error('Error fetching data:', error));
});
