import httpx
import json
import datetime
import os
from bs4 import BeautifulSoup


def jsweather_geturl():
    currentHour = int(datetime.datetime.now().strftime("%H"))
    currentDate = (datetime.datetime.now().strftime("%Y%m%d"))
    if currentHour >= 16:
        currentDate = currentDate + "16"
    elif currentHour >= 6:
        currentDate = currentDate + "06"
    else:
        currentDate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d") + "16"
    url = "http://www.jsweather.com.cn:10000/nriet-kst/zdyb/queryHtml?time=" + currentDate + "&type=TQGB"
    data = json.loads(httpx.post(url).text)
    try:
        weatherurl = str('http://www.jsweather.com.cn:10000' + data["data"][0]["url"])
    except:
        return None
    return weatherurl


def jsweather_getall():
    url = jsweather_geturl()
    if url is None:
        return "获取天气失败", [], []
    soup = BeautifulSoup(httpx.get(url), "html.parser")
    selectors = [
        ("p.Normal--Web-[style='line-height:38.0pt;text-indent:0.0pt;']", 0),
        ("span.Normal[style='color:#000000;font-size:14.0pt;font-family:宋体;mso-bidi-font-family:宋体;']", 0),
        ("p.Normal--Web-[style='line-height:28.0pt;text-indent:0.0pt;']", 0),
        ("span.Normal[style='color:#000000;font-size:14.0pt;font-family:宋体;mso-bidi-font-family:宋体;']", 1),
        ("p.Normal--Web-[style='line-height:28.0pt;text-indent:0.0pt;']", 1),
        ("span.Normal[style='color:#000000;font-size:14.0pt;font-family:宋体;']", 0),
        ("span.Normal[style='color:#000000;font-size:14.0pt;font-family:宋体;']", 1),
        ("span.Normal[style='color:#000000;font-size:14.0pt;font-family:宋体;']", 2),
    ]
    weather_text = ""
    weather_prefix = url.rsplit("/", 1)[0] + "/"
    weather_postfix = "#江苏天气 #江苏气象局 #短期天气预报"
    weather_img_list = []
    for selector, index in selectors:
        elements = soup.select(selector)
        weather_text = weather_text + elements[index].text + "\n"

    img_tags = soup.find_all("img")
    for img in img_tags:
        r = httpx.get(weather_prefix + img["src"], timeout=10)
        with open('/tmp/a.png', 'wb') as f:
            f.write(r.content)
        files = {'uploadfile': (open('/tmp/a.png', 'rb'))}
        r = httpx.post("https://temp.sh/upload", files=files)
        os.remove('/tmp/a.png')
        weather_img_list.append(r.text)
    return weather_text, weather_postfix, weather_img_list
