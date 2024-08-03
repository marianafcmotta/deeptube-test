from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from googleapiclient.discovery import build
from pytube import YouTube

from models import Announcement
from models import requestData

app = FastAPI()
api_key = 'AIzaSyDFmK86-NNtIXvzvtk5KttYWZUyDMRq3YI'
youtube = build('youtube', 'v3', developerKey=api_key)

@app.get('/announcements')
async def get_announcements(data: requestData):

    try:

        request = data.dict()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        adsenses: list[Announcement] = []

        if 'keys' in request and request['keys']:
            for search_key in request['keys']:

                driver.get("https://adstransparency.google.com/?hl=pt-BR&region=BR")

                input_text = driver.find_element(By.CLASS_NAME, "input")    
                input_text.send_keys(search_key + Keys.RETURN)

                time.sleep(4)

                elements = get_options(driver)

                for element in elements:

                    try:
                        url_page = f"https://adstransparency.google.com/?hl=pt-BR&region=anywhere&platform=YOUTUBE&domain={element}"

                        driver.get(url_page)

                        time.sleep(4)

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'priority-creative-grid'))
                        )
                        priority_creative_grid = driver.find_element(By.TAG_NAME, 'priority-creative-grid')

                        if priority_creative_grid:

                            WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.TAG_NAME, 'creative-preview'))
                            )
                            creative_previews = priority_creative_grid.find_elements(By.TAG_NAME, 'creative-preview')

                            for creative_preview in creative_previews:
                                video_indicators = creative_preview.find_elements(By.CLASS_NAME, 'video-indicator')

                                if video_indicators:
                                    video_reference = creative_preview.find_element(By.TAG_NAME, 'a')
                                    ad_url = video_reference.get_attribute('href')
                                    driver.get(ad_url)

                                    WebDriverWait(driver, 10).until(
                                        EC.presence_of_all_elements_located((By.TAG_NAME, 'creative'))
                                    )

                                    creatives = driver.find_elements(By.TAG_NAME, 'creative')

                                    for count in range(len(creatives) - 1):
                                        click_next_button(driver)

                                    time.sleep(5)

                                    last_creative = creatives[-1]

                                    video_url = get_video_url(driver, last_creative)
                                    adsense = get_video_metrics(video_url)

                                    adsenses.append(adsense)
                    except Exception as e:
                        continue

                driver.quit()        

                return adsenses

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_options(driver):

    elements = []

    while True:
        try:
            advertisers_list = driver.find_elements(By.CLASS_NAME, 'advertisers-list')
            
            for advertiser in advertisers_list:
                material_items = advertiser.find_elements(By.TAG_NAME, 'material-select-item')

                for item in material_items:
                    spans = item.find_elements(By.TAG_NAME, 'span')
                    div_containers = item.find_elements(By.CLASS_NAME, 'name-container')

                    if spans:
                        for span in spans:
                            elements.append(span.text.strip())
                            break

                    if div_containers:
                        for div_container in div_containers:
                            divs = div_container.find_elements(By.CLASS_NAME, 'name')

                            for div in divs:
                                elements.append(div.text.strip())
                                break

            return elements

        except StaleElementReferenceException:
            print("StaleElementReferenceException caught. Retrying...")


def click_next_button(driver):
    buttons_skip = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'right-arrow-container'))
    )
    
    for button in buttons_skip:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'right-arrow-container'))
            )
            button.click()

        except StaleElementReferenceException:
            buttons_skip = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'right-arrow-container'))
            )
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'right-arrow-container'))
            )
            button.click()


def get_video_url(driver, last_creative):
    try:
        outer_iframe = last_creative.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(outer_iframe)

        inner_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )

        driver.switch_to.frame(inner_iframe)
        frame_body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        video_iframe = frame_body.find_element(By.ID, 'video')
        video_src = video_iframe.get_attribute('src')

        return video_src

    except Exception as e:
        print(f'Unexpected error: {e}')
        return None
    finally:
        driver.switch_to.default_content()


def get_video_metrics(video_url):
    video_data = youtube.videos().list(part='snippet,contentDetails,statistics', id='WmUsRnhRoNs').execute()
    snippet = video_data['items'][0]['snippet']
    statistics = video_data['items'][0]['statistics']
    content_details = video_data['items'][0]['contentDetails']

    yt = YouTube(video_url)
    transcript = yt.captions.get_by_language_code('br')

    adsense = Announcement()
    adsense.advertiser_name = snippet['channelTitle']
    adsense.title = snippet['title']
    adsense.number_of_views = statistics['viewCount']
    adsense.number_of_likes = statistics['likeCount']
    adsense.duration = content_details['duration']
    adsense.thumbnail_url = snippet['thumbnails']['high']['url']
    adsense.video_url = video_url
    adsense.transcription = transcript.generate_srt_captions() if transcript else 'Transcrição não disponível'
    adsense.is_short = 'shorts' in video_url
    adsense.published_date = snippet['publishedAt']

    return adsense


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)