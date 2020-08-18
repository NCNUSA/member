from backend.models import *


def parse(url, SID, CNAME, VIP):
    """爬蟲抓取該表單網頁，因為使用 js 生成網頁所以使用 Selenium"""
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from selenium.webdriver import FirefoxOptions

    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=opts)
    driver.get(url)
    bsObj = BeautifulSoup(driver.page_source, "html.parser")
    rows = bsObj.find("table").find("tbody").find_all("tr")
    # 每列資料都塞在這裡面
    table = []
    for row in rows:
        columns = row.find_all("td")
        tmp_list = []
        for field in columns:
            tmp_list.append(field.text)
        table.append(tmp_list)
    # Google form 輸出結果第二行會是空白，將之移除
    try:
        table.remove([""] * len(table[0]))
    except:
        pass
    # 判斷姓名是否跟學號匹配
    if SID is not None and CNAME is not None:
        for index, row in enumerate(table):
            if index == 0:
                row.append("姓名是否匹配")
                continue
            try:
                m = Member.objects.get(SID=row[SID - 1])
                if row[CNAME - 1] != m.CNAME:
                    row.append("錯誤(學生會資料庫：" + m.CNAME + ")")
                else:
                    row.append("")
            except:
                row.append("資料庫中尚未有此人")
    # 記得關閉，不然記憶體大爆炸
    driver.quit()
    return table


def add(request):
    title = request.POST["title"]
    url = request.POST["url"]
    gp = request.POST["gp"]
    sid = request.POST["sid"]
    cname = request.POST["cname"]
    vip = request.POST["vip"]
    email = request.POST["email"]
    gp = Group.objects.get(id=gp)

    cname = to_none(cname)
    vip = to_none(vip)
    sid = to_none(sid)
    email = to_none(email)

    if title.strip() != "" and url.strip() != "":
        GoogleSheet.objects.create(
            TITLE=title, URL=url, GP=gp, SID=sid, CNAME=cname, VIP=vip, EMAIL=email
        )
        return True
    else:
        return False


def edit(request):
    title = request.POST["title"]
    url = request.POST["url"]
    gp = request.POST["gp"]
    sid = request.POST["sid"]
    cname = request.POST["cname"]
    vip = request.POST["vip"]
    email = request.POST["email"]
    gp = Group.objects.get(id=gp)

    cname = to_none(cname)
    vip = to_none(vip)
    sid = to_none(sid)
    email = to_none(email)

    if title.strip() != "" and url.strip() != "":
        gs = GoogleSheet.objects.get(id=request.POST["id"])
        gs.TITLE = title
        gs.URL = url
        gs.GP = gp
        gs.SID = sid
        gs.CNAME = cname
        gs.VIP = vip
        gs.EMAIL = email
        gs.save()
        return True
    else:
        return False


def to_none(arg):
    if arg == "":
        arg = None
    return arg
