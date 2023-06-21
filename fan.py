import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("config.ini")

    url = 'http://饭太硬.top/tv'
    response = requests.get(url, headers=headers)
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

    if not match:
        return
    result = match.group(1)

    m = hashlib.md5()
    m.update(result.encode('utf-8'))
    md5 = m.hexdigest()

    try:
        old_md5 = config.get("md5", "conf")
        if md5 == old_md5:
            print("No update needed")
            return
    except:
        pass

    content = base64.b64decode(result).decode('utf-8')
    url = re.search(r'spider"\:"(.*);md5;', content).group(1)
    content = content.replace(url, './JAR/fan.txt')
    content = diy_conf(content)

    with open('xo.json', 'w', newline='', encoding='utf-8') as f:
        f.write(content)
    # 本地包
    local_content = local_conf(content)
    with open('a.json', 'w', newline='', encoding='utf-8') as f:
        f.write(local_content)

    # Update conf.md5
    config.set("md5", "conf", md5)
    with open("config.ini", "w") as f:
        config.write(f)

    jmd5 = re.search(r';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5)
        with open("config.ini", "w") as f:
            config.write(f)

        response = requests.get(url)
        with open("./JAR/fan.txt", "wb") as f:
            f.write(response.content)

def diy_conf(content):
    pattern = r'{"key":"js豆瓣"(.|\n)*(?=\s+\n)'
    replacement = r'{"key":"js豆瓣","name":"🅱豆瓣┃首页","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/drpy.js","searchable": 0,"quickSearch": 0,"filterable": 1},\n'
    content = re.sub(pattern, replacement, content)
    pattern = r'{"key":"csp_Nbys"(.|\n)*(?={"key":"cc")'
    replacement = ''
    content = re.sub(pattern, replacement, content)

    return content

def local_conf(content):
    content = content.replace('http://127.0.0.1:9978/file/tvfan/token.txt', './json/tok.txt')

    return content
if __name__ == '__main__':
    get_fan_conf()