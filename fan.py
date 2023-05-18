import re
import base64
import requests
import hashlib
import configparser
headers = {'User-Agent': 'okhttp/3.15'}

def get_fan_conf():
    config = configparser.ConfigParser()
    config.read("config.ini")

    url = 'http://饭太硬.ga/tv'
    response = requests.get(url, headers=headers)
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

    if not match:
        return
    result = match.group(1)
    content = base64.b64decode(result)

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

    with open('xo.json', 'wb') as f:
        f.write(content)

    # Update conf.md5
    config.set("md5", "conf", md5)
    with open("config.ini", "w") as f:
        config.write(f)

    jmd5 = re.search(b';md5;(\w+)"', content).group(1)
    current_md5 = config.get("md5", "jar").strip().encode()

    if jmd5 != current_md5:
        # Update jar.md5
        config.set("md5", "jar", jmd5.decode())
        with open("config.ini", "w") as f:
            config.write(f)

        url = re.search(b'spider"\:"(.*);md5;', content).group(1)
        response = requests.get(url)
        with open("fan.txt", "wb") as f:
            f.write(response.content)

if __name__ == '__main__':
    get_fan_conf()