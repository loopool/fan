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
    content = content.replace('https://agit.ai/fantaiying/fty/raw/branch/master/JS/drpy1.min.js', './JS/lib/drpy2.min.js')
    pattern = r'{"key":"豆豆".*'
    replacement = r'{"key":"js豆瓣","name":"🅱豆瓣┃首页","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/drpy.js","searchable": 0,"quickSearch": 0,"filterable": 1},'
    content = re.sub(pattern, replacement, content)
    pattern = r'{"key":"Bili"(.)*\n{"key":"Biliych"(.)*\n'
    replacement = ''
    content = re.sub(pattern, replacement, content)
    pattern = r'{"key":"csp_Nbys"(.|\n)*(?={"key":"cc")'
    replacement = ''
    content = re.sub(pattern, replacement, content)

    return content

def local_conf(content):
    pattern = r'{"key":"4KHDR".*'
    replacement = r'{"key":"drpy_js_荐片","name":"荐片[js]","type":3,"api":"./JS/lib/drpy2.min.js","searchable":1,"quickSearch":1,"changeable":1,"ext":"./JS/js/荐片.js","timeout":30},\n{"key":"drpy_js_磁力熊搜索","name":"磁力熊搜索[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/cilixiong.js","searchable":0,"quickSearch":0,"changeable":1},'
    content = re.sub(pattern, replacement, content)
    pattern = r'{"key":"88js"(.|\n)*(?={"key":"YiSo")'
    replacement = r'{"key":"drpy_js_爱看","name":"影视 | 爱看[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/爱看.js"},\n{"key":"drpy_js_美剧网","name":"影视 | 美剧网[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/美剧网.js"},\n{"key":"drpy_js_AGE动漫","name":"动漫 | AGE动漫[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/AGE动漫.js"},\n{"key":"drpy_js_AnFuns","name":"动漫 | AnFuns[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/AnFuns.js"},\n{"key":"drpy_js_NT动漫","name":"动漫 | NT动漫[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/NT动漫.js"},\n{"key":"drpy_js_NyaFun","name":"动漫 | NyaFun[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/NyaFun.js"},\n{"key":"drpy_js_怡萱动漫","name":"动漫 | 怡萱动漫[js]","type":3,"api":"./JS/lib/drpy2.min.js","ext":"./JS/js/怡萱动漫.js"},\n{"key":"百度","name":"百度┃采集","type":1,"api":"https://api.apibdzy.com/api.php/provide/vod?ac=list","searchable":1,"filterable":0},\n{"key":"量子","name":"量子┃采集","type":0,"api":"https://cj.lziapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"非凡","name":"非凡┃采集","type":0,"api":"http://cj.ffzyapi.com/api.php/provide/vod/at/xml/","searchable":1,"changeable":1},\n{"key":"暴風","name":"暴風┃采集","type":1,"api":"https://bfzyapi.com/api.php/provide/vod/?ac=list","searchable":1,"changeable":1},\n{"key":"玉米","name":"玉米┃App","type":3,"api":"csp_AppYsV2","ext":"https://tv.iptv.ski/api.php/app/"},\n{"key":"yaya","name":"鸭鸭┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"https://yayayaaapp.ynf.icu/api.php/app/"},\n{"key":"kuku","name":"酷酷┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://cms.realdou.cn:35264/api.php/app/"},\n{"key":"tiantang","name":"天堂┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://dytt996.com/api.php/app/"},\n{"key":"ruidou","name":"锐豆┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"ext":"http://ys.realdou.cn:2683/api.php/app/"},\n{"key":"酷影视","name":"酷影视┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"https://www.tvkuys.xyz/api.php/app/"},\n{"key":"光影猫","name":"光影猫┃App","type":3,"api":"csp_AppYsV2","searchable":1,"quickSearch":1,"filterable":1,"ext":"http://gymcms.xn--654a.cc/api.php/app/"},\n'
    content = re.sub(pattern, replacement, content)
    return content
if __name__ == '__main__':
    get_fan_conf()