# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

def scrape_reviews():
    driver = webdriver.Chrome()
    url = "https://www.amazon.in/Apple-New-iPhone-12-128GB/dp/B08L5TNJHG/"
    driver.get(url)
    time.sleep(3)

    # Click on "See all reviews" link
    try:
        all_reviews_link = driver.find_element(By.XPATH, '//a[contains(@data-hook, "see-all-reviews-link-foot")]')
        all_reviews_link.click()
        time.sleep(3)
    except:
        print("All reviews link not found or could not be clicked.")

    # Set up CSV file
    with open("reviews.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Reviewer Name", "Review Title", "Review Text", "Style Name", "Color", "Verified Purchase"])

    # Loop to scrape multiple pages of reviews
    for _ in range(5):  # Adjust range for the number of pages to scrape
        reviews = driver.find_elements(By.XPATH, '//div[@data-hook="review"]')

        for review in reviews:
            try:
                reviewer_name = review.find_element(By.XPATH, './/span[@class="a-profile-name"]').text.strip()
            except:
                reviewer_name = ""
            try:
                title = review.find_element(By.XPATH, './/a[@data-hook="review-title"]').text.strip()
            except:
                title = ""
            try:
                text = review.find_element(By.XPATH, './/span[@data-hook="review-body"]').text.strip()
            except:
                text = ""
            try:
                style = review.find_element(By.XPATH, './/a[contains(@class, "review-data")]').text.strip()
            except:
                style = ""
            try:
                color = review.find_element(By.XPATH, './/a[contains(@class, "a-size-mini a-link-normal a-color-secondary")]').text.strip()
            except:
                color = ""
            try:
                verified = "Yes" if review.find_element(By.XPATH, './/span[@data-hook="avp-badge"]').is_displayed() else "No"
            except:
                verified = "No"

            # Write review to CSV file
            with open("reviews.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([reviewer_name, title, text, style, color, verified])

        # Click "Next" to go to the next page
        try:
            next_button = driver.find_element(By.XPATH, '//li[@class="a-last"]/a')
            next_button.click()
            time.sleep(3)
        except:
            print("No more pages or 'Next' button not found.")
            break

    driver.quit()

if __name__ == "__main__":
    scrape_reviews()
    print("Scraping completed and saved to reviews.csv")
