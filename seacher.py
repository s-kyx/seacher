import asyncio
import aiohttp
import time
import sys
from bs4 import BeautifulSoup
import re
import aiofiles
import urllib.parse
import argparse
from colorama import init, Fore
import ssl

bingheaders = {
    'cookie': """USRLOC=; MUID=186B70A03A036EE939FB63113B656FED; elt={"access_token":"eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkExMjhDQkMtSFMyNTYiLCJ4NXQiOiJEZTRNSWJTY1ExeTdMYlBGSVR3emNMRmxrcFkiLCJ6aXAiOiJERUYifQ.S-BEDsRGCKt8a6ih561A8XnFCHF9NdFjHzJLdNYjEFgB1dxXmc49SE2-4OjR9_hjVgR6zc20NqxUHdpJ4DCAq4MCsaOSjR1rd9yBdrq3zY6Uk8kaQkdaMvf7lDjf6gLIrWxgpOlqeNvy9MtuPShozBU4JcT3YQ7_W2zT1ISteQaEWPXrpxHQQgnlQoCPcioTEU6lRXQI5Lgz-6sSt7GKyci8B3HMbvkNDbvRVd6CwuBj9BRONJWpI0JwVrvfWfKae4KIIB9tAf3pQ7BcOz-RxK0T5T6-cLBh3wCcNX2OwRZhgKXmw0Hd8PYueeo7YgXDSXsJY3x3iI-Gz4KNTDFpng.BzkuhRhLInLPIAnxGCzVdw.oRtiLqngzVLJqn5qOK7WyVuz_a7MqWJgdWzC2JNrKl00xbuTBk1mtIiomX6chkMqTfUNhSPm9W2qhPawNrfZsyQbScT7f8VcfkdPBI_vmW-yHSSFEXedWkzcFxTwOYQizjL_gc8ksv42e4qgUBxQAfpihty43ZQqjOdzjio24PnI0PoYPakDOEX_A8D_7b27QyBuyAG5HJ-re7TafWNJ1vl0ty4a2uJb4FDk86c6_oWK5bHUXubDUixt-7efy4ZM_LRGTFl3n1TfW29HSjD778VsS2pQGAH-P49vcH7ktHFUGRgLKrFhfmWzw6jSsCFzk74ozDMIAmlHnReFDnAjTuNRAaxPNZ757aLJmDopPA-yuyJStWazjCtsr_lKoHfH3TpomJOkn9NtHIrovyntw3m7rBZk_pz8KjDB8xgeAV6uHNXaLwGvYxSKeMVOAN9c7qu9kdhM_TcxlCYBjIH6E6pNIOeNtXXFph-nGP5Wqzt8p-ctmfx6oZSoRF9DZEIshO2Nq5UGX0nfeAUJIOxJQ27AeVOSQyh2amEJgF_R_a5mG8A1f5Q8usVg8458JcH5SZxgIPwioNCjQTXLJwUhEtXNFLDadTSn-i7LKSxYNapeAmzrUOWB0jAHM7udS7f0V5cBW52LqKkjIHCHGI3hVBLhcx661CCn6r_LBBCb4g_BAXuA5BpXY0ieuJWfX2lYRnAuJ7342pIDR1XFjOFAu6UxSXfOR1nsAdBRTelMlzLDbkd-VwxuHqa8ldrELj3POUy4mNX_D2E2vezaWoGEB4FTCYr83Tih1-sYp1d1QGZyL6SHfYc1A5OM3omrrDIecaMKfU78ec_zth-kuHIlblmjIAVsMVwFIGWRtzyto7pO1SZdMsakkUIUKLKW4bFkR6gZk5yo-AdU1HmBCPmO2tf6HTgaKFK99HlsO2M3aoAJ7tTAwGmjkFDt7xSIcykjPyRXY0a8HQ0GXoc4BzOfcaEYqkWzAo5Cwrfd04PMWiso42_AXohss1fzDYZam_znUmSL1jbMJH_8pUP8hJGdozBJhDLMG2xtEtvDU7PMAi4ko6a_j-9Iyhh_6gMVDZYrbpFbVjWsmDCU_V4fZS1J7vTTekXBvcWyqjMdCDW-Dp7ks2GBRkMDHcYR1MzmbhhONz-C1iX8xe-qhKL8aOoB54w_kOoOESrbooca8o4in2nHYSBOFXOeomR8BHro3DwMpY6gf5HsnLAJcnUuTKwBH4N9q0JsrepOR6M7oSU7BPrIoxt_lXbQed7gddfD2ilPw3LVlb8Rnm_0xosY6QnbJqpWc6_oSDCuoE4IAhWfrfwS1iQqj1LcCrVzR5QQ9Lox4zXObPiEpDz14Vc_QKBQbQ.WO0hHPJ4bxMyMCkPKg3AJA","account_type":"MSA","login_hint":"2858418450@qq.com","e":"bfd58970"}""",
    'referer': 'https://cn.bing.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.0'}

baiduheaders = {
    'Cookie': """BIDUPSID=4AB4B4749F6B76D0983DCF2FEE3663E4; PSTM=1697882386; BAIDUID=4AB4B4749F6B76D04A0941096B68FCAC:FG=1; BD_UPN=12314753; BDUSS=S1OTFZHYzBGVjQ0Q2ZTR3UybS1-TFhXanZ0LXJ2b1F2SlVWQ3VUa29XfjU4MmRsRVFBQUFBJCQAAAAAAAAAAAEAAAAOTAGXzLG1vcKZwZS1hgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPlmQGX5ZkBla; BDUSS_BFESS=S1OTFZHYzBGVjQ0Q2ZTR3UybS1-TFhXanZ0LXJ2b1F2SlVWQ3VUa29XfjU4MmRsRVFBQUFBJCQAAAAAAAAAAAEAAAAOTAGXzLG1vcKZwZS1hgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPlmQGX5ZkBla; BAIDUID_BFESS=4AB4B4749F6B76D04A0941096B68FCAC:FG=1; MBDFEEDSG=4861c562486bcdd5511c17926d0bb984_1699343290; ab_sr=1.0.1_Njk4ZjQ5Y2M1YmMxZDBiOGZmMzFlYmEzMzRhMmY3YTYwYTJiZGI5OTdjZGNkMmM5MTg4ZjY0MjFiNzU1OGZlMDYxNjJjNjg3NTk3YTYyOGE5MjQzMDRkNDUzZGM4YTdmNDhkZmU2MDUwYWMzOWQxZjJmOGE5OGZiYzFkMzU1YTZhODE5ZWNkYTRiOGY2MTI2NTg0ZmI4MDdmYTI0YWQxOA==; BA_HECTOR=848k2ha58ka5ak05a0ak85a11ikjt1a1q; ZFY=wklH6L6KQz:BZuOmhacX4eJBlZz4M7iHumdQKDFJIto0:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598""",
    'Host': 'www.baidu.com',
    'referer': 'https://www.baidu.com/s',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
}

start = time.time()


def printascii():
    # 初始化
    init()
    # 设置颜色
    print(Fore.GREEN + '''
     # # # # #  # # # # # # # # # # # # # # # # 
    #                        _                 #
    #                       | |                #             
    #    ___  ___  __ _  ___| |__   ___ _ __   #
    #   / __|/ _ \/ _` |/ __| '_ \ / _ \ '__|  #
    #   \__ \  __/ (_| | (__| | | |  __/ |     #
    #   |___/\___|\__,_|\___|_| |_|\___|_|     #
    #                                          #
    #                                          #
     # # # # # # # # # # # # # # # #  # # # # #         

                                               proved by Skyx
                                                   2023.11.7  
                                                   ''' + Fore.RESET)


def commend():
    parser = argparse.ArgumentParser(prog="Seacher", description='此工具用于对百度和必应搜索的协程爬取', usage='please read -h')
    parser.add_argument("-k", type=str, help="搜索的关键词", nargs='+')
    # 添加一个positional arguments，叫a,读取类型为int（默认是字符串）
    parser.add_argument("-p", type=int, help="需要搜索页数,默认为5", default=5)
    # parser.add_argument("-t", '--task', type=int, help="设置的线程,默认为8", default=8)
    parser.exit_on_error = False
    args = parser.parse_args()
    if len(sys.argv) == 1:
        printascii()
        parser.print_help()
        sys.exit()
    return args


async def getallone(url):
    url_list = []
    title_list = []
    async with aiohttp.ClientSession() as session:
        print('正在爬取:' + url)
        async with session.get(url, headers=bingheaders) as resp:
            a = await resp.text()
            # print(a)
            # await asyncio.sleep(0.5)
            soup = BeautifulSoup(a, 'lxml')
            h2a = soup.select('h2 a')
            # urls=soup.select('a.tilk')
            for h in h2a:
                # print(h.text)
                htext = h.text.replace('\n', '').replace(',', ' ').strip()
                title_list.append(htext)
                url_list.append(h.get('href'))

    return url_list, title_list


async def bingwriteCSV(titles, links, keyword):
    infos = list(zip(titles, links))
    pattern = r"[\\/:\*\?\"<>|]"
    keyword = re.sub(pattern, "", keyword)
    async with aiofiles.open(f'./{keyword}.csv', 'at', newline='', encoding='utf_8_sig') as file:
        await file.write("\n以下为必应的爬取结果:\n标题,url" + "\n")
        for row in infos:
            await file.write(",".join(row) + "\n")
    # print("bingCSV文件已保存!")


async def bingmain(keyword, num):
    print('必应爬取任务进行中...\n')
    urllist = []
    titlelist = []
    tasks = []
    num = num * 10
    for pn in range(0, num, 10):
        url = f'https://cn.bing.com/search?q={keyword}&first={pn}'
        tasks = tasks + [asyncio.create_task(getallone(url))]
    resule = await asyncio.gather(*tasks)
    for i in range(int(num / 10)):
        urllist += resule[i][0]
        titlelist += resule[i][1]
    print('标题\t                                    URL\t')
    for title, url in zip(titlelist, urllist):
        print("{}\t {}\t\n".format(title, url), end='')
    await bingwriteCSV(titlelist, urllist, keyword)
    print(Fore.GREEN + '必应爬取任务完成\n' + Fore.RESET)


async def gettrueurl(url):
    try:
        domain = 'https://www.baidu.com/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=baiduheaders, allow_redirects=False) as resp:
                await resp.text()
                if str(resp.headers.get('Location')) != None and str(resp.headers.get('Location')) != '':
                    return str(resp.headers.get('Location'))
                else:
                    print(url + '该url无法转跳')
                    url = urllib.parse.urljoin(domain, url)
                    return url
    except:
        return url


async def baiduwriteCSV(titles, links, keyword):
    infos = list(zip(titles, links))
    pattern = r"[\\/:\*\?\"<>|]"
    # 使用正则表达式替换不允许的字符为空字符串
    keyword = re.sub(pattern, "", keyword)
    async with aiofiles.open(f'./{keyword}.csv', 'at', newline='', encoding='utf_8_sig') as file:
        await file.write("\n以下为百度的爬取结果:\n标题,url" + "\n")
        for row in infos:
            await file.write(",".join(row) + "\n")
    # print("baidu-CSV文件已保存!")


async def getfirstinfo(keyword, pn):
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE
    titlelist = []
    fakeurl = []
    Source = []
    url = f'http://www.baidu.com/s?wd={keyword}&pn={pn}'
    print(f'正在爬取{url}')
    while 1:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=baiduheaders, ssl=sslcontext) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'lxml')
                    h3 = soup.select('h3.t')

                    for h3 in h3:
                        h3text = h3.text.replace('\n', '').replace(',', ' ').replace('\ue636', '').strip()
                        titlelist.append(h3text)
                        fakeurl.append(h3.a.get('href'))
            return titlelist, fakeurl
        except:
            print("baidu链接失败，正在重新尝试...")


async def baidumain(keyword, num):
    print('百度爬取任务进行中...\n')
    urllist = []
    titlelist = []
    tasks1 = []
    tasks2 = []
    Source = []
    num = int(num * 10)
    for i, pn in enumerate(range(0, num, 10)):
        tasks1 = tasks1 + [asyncio.create_task(getfirstinfo(keyword, pn))]
    result = await asyncio.gather(*tasks1)
    for i in range(int(num / 10)):
        # print(result[i][1])
        titlelist += result[i][0]
        # Source +=result[i][2]
        for url in result[i][1]:
            if not url.startswith(('http://', 'https://')):
                domain = 'http://www.baidu.com/'
                url = urllib.parse.urljoin(domain, url)
            tasks2 = tasks2 + [asyncio.create_task(gettrueurl(url))]
    await asyncio.sleep(0.5)
    urllist += await asyncio.gather(*tasks2)
    print('标题\t                                     URL\t')
    for title, url in zip(titlelist, urllist):
        print("{}\t {}\t \n".format(title, url), end='')
    await baiduwriteCSV(titlelist, urllist, keyword)
    print(Fore.GREEN + '百度爬取任务完成！\n' + Fore.RESET)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    args = commend()
    keyword = args.k
    num = args.p
    keywords = ""
    for key in keyword:
        keywords = keywords + key + " "
    keywords = keywords.strip()
    printascii()
    loop.run_until_complete(bingmain(keywords, num))
    # asyncio.sleep(0.5)
    loop.run_until_complete(baidumain(keywords, num))
    print(Fore.GREEN + '总任务结束!' + Fore.RESET)
    end = time.time()
    print(Fore.RED + '脚本总时间:', end - start)
