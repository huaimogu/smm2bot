import requests


def down_file(url, path, proxies=None):
    headers = {
        'authority': 'cl.bc53.xyz',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    try:
        r = requests.get(url, stream=True, headers=headers, proxies=proxies, timeout=5)
        code = r.status_code
        print('download file: {0} , result code {1}'.format(url, code))
        i = 0
        while code != 200 and i < 1:
            r = requests.get(url, stream=True, headers=headers, proxies=proxies)
            code = r.status_code
            i = i + 1
        if code == 200:
            error = None
        else:
            error = r.text
        with open(path, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
        return [code, error]
    except Exception as e:
        return [-1, str(e)]
