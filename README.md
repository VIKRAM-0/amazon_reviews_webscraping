# Description Of Problem Statement
The problem statement focus on developing a system which would allow us to web scrap reviews from amazon and perform sentimental analysis on the reviews.
# Technologies used
> FastApi

> Selenium

> NLTk
### FastApi
Here fastapi is used to create endpoints for the process which would allow us for the reterival and the sentimental analysis. This is used to develop the query and the endpoint Api's.

### Selenium
As amazon uses verification for their website and this makes normal web scraping difficult by selenium we would be able to create a virtual chrome window and from that we would be able to web scrap the contents or the reviews.

### NLTK
This is a module present in python through which we would be able to perform Natural language processing tasks.The use of this in the project is to analyze the sentiments of the reviews which would be classified as postive or negative.

# Runing the application
1. The first step after cloning the respository is to run the `scraper.py` file.
2. After that the values would be stored in the `reviews.csv` file.
3. The next step is to process the data which is collected from the web scrap.
4. So now run the `process_data.py` file.
5. Now every process is done the only step now is to start the application.
6. Open the terminal and run the commad `uvicorn main:app --reload`.
7. After this process the link would be given.
8. Follow the link to open the application. The link would look like this `INFO:     Uvicorn running on http://127.0.0.1:8000 `.
9. To quit the application press `ctrl + c ` in the terminal
