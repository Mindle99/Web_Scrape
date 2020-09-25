from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd
from bs4 import BeautifulSoup


driver = webdriver.Chrome("./chromedriver")

dataframe = pd.DataFrame(columns=["Title","Location","Company","Rating","Salary","Description"])

max_results_per_city = 500
job_set = ['Data+Scientist','Data+Analyst','Data+Engineer','Business+Analyst','Machine+Learning+Engineer',"Big+Data+Engineer","Data+Architect","Business+Intelligence+Analyst","Statistician"]


for jobs in job_set:
    for i in range(0, max_results_per_city,10):
        driver.get("https://ca.indeed.com/jobs?q="+str(jobs)+"&l=Ontario&start="+str(i))
        driver.implicitly_wait(4)

        all_jobs = driver.find_elements_by_class_name('result')

    
        for job in all_jobs:

            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html,'html.parser')

            try:
                title = soup.find("a", class_="jobtitle").text.replace('\n','')
            except:
                title = 'None'
            try:
                location = soup.find(class_="location").text
            except:
                location = 'None'
            try:
                company = soup.find(class_="company").text.replace('\n','').strip()
            except:
                company = 'None'
            try:
                rating = soup.find("a", class_="ratingNumber").text.replace('\n','').strip()
                #rating = driver.find_element_by_xpath('//*[@id="p_a757e4ec868d50aa"]/div[1]/div[1]/span[2]')
            except:
                rating = 'None'
            try:
                salary = soup.find(class_="salary").text.replace('\n','').strip()
            except:
                salary = 'None'
                
            sum_div = job.find_elements_by_class_name("summary")[0]

            try:
                sum_div.click()
            except:
                close_popup = driver.find_element_by_id("popover-x")
                close_popup.click()
                sum_div.click()
                
            job_desc = driver.find_element_by_id('vjs-tab-job').text

            dataframe = dataframe.append({'Title':title,'Location':location,
                            'Company':company,'Rating':rating, 'Salary':salary,"Description":job_desc}, 
                            ignore_index=True)

dataframe.to_csv("indeed_jobs.csv", index=False)