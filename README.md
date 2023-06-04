# URL-Shortener-Service
A simple URL shortener service built with Python, Flask, MySQL, and Docker.

## Description
The URL Shortener Service is a web application that allows users to shorten long URLs into more concise 
and manageable links. It provides a user-friendly interface to input a long URL and generate a unique 
short URL that redirects to the original URL. Additionally, the service offers a set of APIs for programmatic interaction.

## API Endpoints
* __`POST /shorten_url`__: Accepts a JSON payload with the long URL,<br/>e.g., `{"long_url": "https://www.example.com/long_url"}`
 and returns the shortened URL as a response, <br/>e.g., `{short_url": "http://127.0.0.1:5000/abc123}`.
* __`GET/`__: Retrieves statistics for a given short URL, e.g., `{/abc123}`.


## How to run
To run the URL shortener service locally, follow these steps:
1. Clone the repository: `git clone https://github.com/neetusuthar90/URL-Shortener-Service`
2. `docker-compose up`
3. Access the URL shortener service at http://localhost:8000.
4. API endpoint is available at http://localhost:5000.
