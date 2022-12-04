from aip import AipOcr

def BaiduOcr(_img, _appid='', _apikey='', _secretkey='', _options=None) -> str:
    if _appid and _apikey and _secretkey:
        client = AipOcr(_appid, _apikey, _secretkey)
    else:
        return

    result_text = ''
    try:
        result = client.general(_img, _options)
        print(result)
        if 'words_result' in result:
            for res in result['words_result']:
                result_text += res['words']
                result_text += '\n'
        else:
            result_text = result
    except:
        result_text = u'网络连接失败！'

    return result_text

