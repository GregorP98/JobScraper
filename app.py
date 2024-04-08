from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_jobs(keyword, location):
    url = f"https://www.indeed.com/jobs?q={keyword}&l={location}"
    response = requests.get(url)
    job_listings = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_elements = soup.find_all('div', class_='jobsearch-SerpJobCard')

        for job_element in job_elements:
            title_element = job_element.find('h2', class_='title')
            company_element = job_element.find('span', class_='company')
            location_element = job_element.find('span', class_='location')
            if None in (title_element, company_element, location_element):
                continue
            title = title_element.text.strip()
            company = company_element.text.strip()
            location = location_element.text.strip()
            link = "https://www.indeed.com" + title_element.a['href']
            job_listings.append({"title": title, "company": company, "location": location, "link": link})

    return job_listings

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        location = request.form['location']
        job_listings = scrape_jobs(keyword, location)
        return render_template('index.html', job_listings=job_listings, keyword=keyword, location=location)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
