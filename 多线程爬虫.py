import threading, time, random, requests, re
import pandas as pd


titles = []
three_prices = []
prices = []

def download(urls, headers, lock):

    for url in urls:
        lock.acquire()
        time.sleep(random.randint(5, 10))
        req = requests.get(url=url, headers=headers)

        titles.extend(re.findall(r'pic\\" title=\\"(.*?)\\">\\n', req.text))
        three_prices.extend(re.findall(r'30天成交<em>(.*?)<\\/em><span>元', req.text))
        prices.extend(
            re.findall(r'<span class=\\"sm-offer-priceNum sw-dpl-offer-priceNum\\" title=\\"&yen;(.*?)\\">', req.text))
        lock.release()


def save(lock):

    while True:
        try:
            lock.acquire()
            data = {
                'titles': titles,
                'three_prices': three_prices,
                'prices': prices
            }
            df = pd.DataFrame(data)
            df.to_excel(r'C:\Users\Administrator\Desktop\佳丽姐\可剥指甲油19号.xlsx')
            lock.release()
        except Exception:
            break


def main():
    lock = threading.Lock()
    urls = []
    for i in range(0, 160, 20):
        my_url = 'https://s.1688.com/selloffer/rpc_async_render.jsonp?descendOrder=true&sortType=va_rmdarkgmv30rt&uniqfield=userid&keywords=%BF%C9%B0%FE%D6%B8%BC%D7%D3%CD&earseDirect=false&netType=1%2C11&n=y&templateConfigName=marketOfferresult&offset=0&pageSize=60&asyncCount=20&startIndex=' + str(
            i) + '&async=true&enableAsync=true&rpcflag=new&_pageName_=market&callback=jQuery172015973359135540788_1555641880038'
        urls.append(my_url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': '__sw_ktsz_count__=1; cna=uUM8FZanjjgCAduJy+BpF6fG; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E5%A1%9E%E7%93%A6%E6%96%AF%E7%9A%84%E5%95%8A; UM_distinctid=16a29ea582e6a3-0b7eb08ead8e14-651a107e-1fa400-16a29ea582f55a; ali_ab=219.137.203.223.1555481619955.4; ali_apache_track=c_mid=b2b-1828564353|c_lid=%E5%A1%9E%E7%93%A6%E6%96%AF%E7%9A%84%E5%95%8A|c_ms=1; last_mid=b2b-1828564353; __rn_alert__=false; alisw=swIs1200%3D1%7C; h_keys="%u53ef%u5265%u6307%u7532%u6cb9#%u93b8%u56e9%u6573%u5a0c?#%u93b8%u56e9%u6573%u5a0c%u7b6fttps://s.1688.com/selloffer/offer_search.htm?keywords=%u93b8%u56e9%u6573%u5a0c?#%u93b8%u56e9%u6573%u5a0c%u7b6fttps://s.1688.com/selloffer/offer_search.htm?keywords=%u93b8%u56e9%u6573%u5a0c%ufffd#%u732b%u773c%u80f6#%u6307%u7532%u6cb9#%u53ef%u5378%u7532%u6cb9%u80f6"; cookie2=19d2cf941325367e6ddf0956d3967fc6; t=49af0bd19d2c1b082c435ad20d9dc1b5; _tb_token_=71dfbe66e1557; __cn_logon__=false; alicnweb=touch_tb_at%3D1555487977201%7ChomeIdttS%3D30837404186370153862528232204433005880%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E5%25A1%259E%25E7%2593%25A6%25E6%2596%25AF%25E7%259A%2584%25E5%2595%258A%7Cshow_inter_tips%3Dfalse; _csrf_token=1555488229145; __wapcsf__=1; _bl_uid=yqjC5uvUk40yad266j2n27ji2vpz; ad_prefer="2019/04/17 16:23:04"; isg=BAcHZRJrFyjEbpOks0ognAiTlrt9B9sWjb6NHdn0AxaqSCYK4dzNPAhO7mizoLNm; l=bBPFC2wHv3lRbzsfBOCgZQd_ab7ORIRfguSRfNV9i_5dFsY0g0_OlaykoUv6Vj5POw8B4Q6MVtpTCeng5PHf.'
    }
    t1 = threading.Thread(target=download,args=(urls,headers, lock))
    t2 = threading.Thread(target=save, args=(lock, ))
    t1.start()
    t2.start()

if __name__ == '__main__':
    main()
