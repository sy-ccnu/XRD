#-*- coding = utf-8 -*-

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.response
import xlwt
import sqlite3



def main():
    #爬取网页
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = r"豆瓣电影TOP250.xls"
    # #保存数据
    saveData(datalist,savepath)

#影片链接
findlink = re.compile(r'<a href="(.*?)">')     #创建正则表达式，表示查找的字符串规则
#影片封面
findImgSrc = re.compile(r'<img.*src="(.*?)".*/>',re.S)      #re.S让换行符包含在字符串中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评分人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>',re.S)
#影片详情
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


def getData(baseurl):
    datalist = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    }
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url, headers)
    # 逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []       #保存一部电影的信息
            item = str(item)

            link = re.findall(findlink,item)[0]     #通过正则表达式查找指定字符串
            data.append(link)

            ImgSrc = re.findall(findImgSrc,item)[0]
            data.append(ImgSrc)

            Title = re.findall(findTitle,item)
            if(len(Title)==2):
                cTitle = Title[0]
                data.append(cTitle)
                oTitle = Title[1].replace("/","")       #替换无用信息为空
                oTitle =oTitle.replace("\xa0","")
                data.append(oTitle)
            else:
                data.append(Title[0])
                data.append("")         #外文名留空

            Rating = re.findall(findRating,item)[0]
            data.append(Rating)

            Judge = re.findall(findJudge,item)[0]
            data.append(Judge)

            Inq = re.findall(findInq,item)
            if(len(Inq)!=0):
                data.append(Inq[0])
            else:
                data.append("")


            Bd = re.findall(findBd,item)[0]
            Bd = re.sub("<br(\s+)?/>(\s+)?"," ",Bd)
            Bd = re.sub("/"," ",Bd)
            Bd = re.sub('\xa0'," ",Bd)
            data.append(Bd.strip())         #去掉前后的空格

            datalist.append(data)
            #print(item)
    #print(datalist)
    return datalist

def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)        #创建Wordbook对象
    sheet = book.add_sheet('豆瓣电影TOP250',cell_overwrite_ok=True)     #创建工作表
    col = ("影片链接","影片封面","影片片名","影片外国名","影片评分","评分人数","影片概况","影片详情")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

    print("save...")
    print("保存完成！")

def askURL(url,headers):
    request = urllib.request.Request(url = url,headers = headers)
    try:
        response = urllib.request.urlopen(request,timeout = 1)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLerror as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html




#调用函数
if __name__ == "__main__":
    main()
    print("爬取完毕！")
















