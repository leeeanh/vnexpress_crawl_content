from symbol import continue_stmt
import json
import requests
from bs4 import BeautifulSoup

# category = []
# thoi_su, goc_nhin, the_gioi, kinh_doanh, giai_tri, the_thao, phap_luat, giao_duc, suc_khoe, doi_song, du_lich, khoa_hoc, so_hoa, xe, y_kien, tam_su, cuoi= ([] for i in range(17))
def categories(ctg):
        # if ctg == "https://video.vnexpress.net" or ctg == "https://raovat.vnexpress.net": continue
    array=[]
    if ctg == "https://vnexpress.net/goc-nhin": get_goc_nhin(array)
    elif ctg == "https://vnexpress.net/y-kien": links(ctg, array)
    else:
        print("L" + ctg) 
        links(ctg, array)
        second_links(ctg, array)
    return array
def get_goc_nhin(arr):
    # for i in range(1, 67):
    for i in range(1, 5):
        url = "https://vnexpress.net/ajax/goc-nhin?category_id=1003450&page=" + str(i) + "&exclude=3&rule=2"
        request_database(url,arr)

def second_links(url, arr):
    session = requests.session()
    webpage = session.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')
    sub_menu = soup.find(id='sub_menu')
    for ctg in sub_menu.find_all('a'):
        ctgy = ctg.get('href').encode('utf-8')
        if "https://" not in ctg.get('href').encode('utf-8'):
            ctgy = "https://vnexpress.net" + ctg.get('href')
        if (ctgy=="https://video.vnexpress.net/giai-tri" or ctgy=="https://video.vnexpress.net/the-thao" or ctgy=="https://vnexpress.netjavascript:;" or ctgy=="https://vnexpress.net/interactive/2016/bang-gia-xe" or ctgy=="https://vnexpress.net/interactive/2017/bang-gia-xe-cu" or ctgy=="https://vnexpress.net/interactive/2016/bang-gia-xe-may" or ctgy=="https://raovat.vnexpress.net/oto" or ctgy=="https://vnexpress.net/oto-xe-may/thi-bang-lai" or ctgy=="https://vnexpress.net/the-thao/du-lieu-bong-da" or ctgy=="https://vnexpress.net/the-thao/photo" or ctgy=="https://vnexpress.net/du-lich/anh-video" or ctgy=="https://vnexpress.net/so-hoa/video"
            or ctgy=="https://vnexpress.net/giao-duc/trac-nghiem" or ctgy=="https://vnexpress.net/giao-duc/trac-nghiem" or ctgy=="https://vnexpress.net/suc-khoe/cac-benh/ung-thu" or ctgy=="https://vnexpress.net/giai-tri/the-oscars" or ctgy=="https://vnexpress.net/giai-tri/thu-vien"):
            continue
        elif ctgy == "https://vnexpress.net/thoi-su/nong-nghiep-sach":
            nong_nghiep_sach(ctgy, arr)
        elif ctgy == "https://vnexpress.net/the-thao/vleague-2018" or ctgy == "https://vnexpress.net/bong-da/asian-cup-2019":
            asian_cup_AND_vleague(ctgy, arr)
        elif ctgy == "https://vnexpress.net/giao-duc/tuyen-sinh":
            tuyen_sinh(ctgy, arr)
        elif ctgy == "https://startup.vnexpress.net":
            start_up(arr)
        elif ctgy=="https://vnexpress.net/doi-song/to-am" or ctgy=="https://vnexpress.net/doi-song/loi-song" or ctgy=="https://vnexpress.net/doi-song/nha" or ctgy=="https://vnexpress.net/doi-song/tieu-dung" or ctgy=="https://vnexpress.net/du-lich/cam-nang":
            links(ctgy, arr)
        else:
            links(ctgy, arr)
            third_links(ctgy, arr)
def third_links(url, arr):
    session = requests.session()
    webpage = session.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')
    main = soup.find(class_='sub_breadcrumb left')
    if(main == None): continue_stmt
    else:
        for ctg in main.find_all('a', href=True):
            ctgy = "https://vnexpress.net" + ctg.get('href').encode('utf-8')
            if ("javascript:;" in ctg.get('href').encode('utf-8')
                or ctgy == "https://vnexpress.net/bong-da/asian-cup-2019"
                or ctgy == "https://vnexpress.net/giao-duc/giao-duc-40/quiz-game"
                or ctgy == "https://vnexpress.net/du-lich/quoc-te/khac" or ctgy == "https://vnexpress.net/du-lich/viet-nam/khac"):
                continue
            elif ctgy == "https://vnexpress.net/suc-khoe/han-che-lam-dung-khang-sinh":
                han_che_lam_dung_khang_sinh(ctgy,arr)
            else:
                links(ctgy, arr)

def nong_nghiep_sach(url, arr):
    session = requests.session()
    webpage = session.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')
    main = soup.find(class_="container clearfix")
    for ctg in main.find_all('a', href=True):
        if(ctg.parent.parent.parent.name == "nav"):
            ctgy = "https://vnexpress.net" + ctg.get('href').encode('utf-8')
            print ("L"+ctgy)
            nong_nghiep_sach_links(ctgy, arr)
def nong_nghiep_sach_links(url, arr):
    global i
    session = requests.session()
    webpage = session.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')
    main = soup.find(class_="content-main").find_all(class_="title_news")
    for ctg in main:
        print(ctg.find('a', href=True).get('href')) 
        arr.append(ctg.find('a', href=True).get('href').encode('utf-8'))
    next = soup.find('a', href=True, class_='next')
    if next == None:
        continue_stmt
    else:
        link_next = "https://vnexpress.net" + next.get('href').encode('utf-8')
        nong_nghiep_sach_links(link_next, arr)
def asian_cup_AND_vleague(url1,arr):
    session = requests.session()
    webpage = session.get(url1).text
    soup = BeautifulSoup(webpage, 'html.parser')
    main = soup.find(class_="main_menu_seagame width_common")
    for ctg in main.find_all('a'):
        ctgy = ctg.get('href').encode('utf-8')
        if(ctgy == "https://vnexpress.net/bong-da/asian-cup-2019/lich-thi-dau" or ctgy == "https://vnexpress.net/bong-da/asian-cup-2019/bang-diem"):
            continue
        else:
            print("L" + ctgy)
            if ctgy=="https://vnexpress.net/bong-da/asian-cup-2019":                    maxpage = 14
            elif ctgy=="https://vnexpress.net/bong-da/asian-cup-2019/tin-tuc":          maxpage = 15
            elif ctgy=="https://vnexpress.net/bong-da/asian-cup-2019/anh":              maxpage = 4
            elif ctgy == "https://vnexpress.net/bong-da/asian-cup-2019/video":          maxpage = 3
            elif ctgy=="https://vnexpress.net/bong-da/asian-cup-2019/binh-luan":        maxpage = 4
            elif ctgy=="https://vnexpress.net/the-thao/vleague-2018/tin-tuc#1004190":   maxpage = 15
            elif ctgy=="https://vnexpress.net/the-thao/vleague-2018/anh#1004180":       maxpage = 2
            elif ctgy=="https://vnexpress.net/the-thao/vleague-2018/video#1004181":     maxpage = 10
            elif ctgy =="https://vnexpress.net/the-thao/vleague-2018/ben-le#1004182":   maxpage = 4
            elif ctgy == "https://vnexpress.net/the-thao/vleague-2018/binh-luan#1004191":maxpage = 3
            else: continue
            for i in range(1, maxpage):
                if ctgy=="https://vnexpress.net/bong-da/asian-cup-2019":
                    url = "https://vnexpress.net/the-thao/affcup2018/morenews/category_id/1004308/page/" + str(i) + "/catecode/home/exclude/3875583,3875377,3875533,3875475,3875223,3875346,3875382,3874952,3874329,3874301,3873405,3873547,3875202,3873572,3873561,3873553,3873331"
                elif ctgy=="https://vnexpress.net/bong-da/asian-cup-2019/tin-tuc":
                    url = "https://vnexpress.net/the-thao/affcup2018/morenews/category_id/1004309/page/" + str(i) + "/catecode/tin/exclude"
                elif ctgy=="https://vnexpress.net/bong-da/asian-cup-2019/anh":
                    url = "https://vnexpress.net/the-thao/affcup2018/morenews/category_id/1004310/page/" + str(i) + "/catecode/anh-video/exclude"
                elif ctgy=="https://vnexpress.net/bong-da/asian-cup-2019/video":
                    url = "https://vnexpress.net/the-thao/affcup2018/morenews/category_id/1004311/page/" + str(i) + "/catecode/anh-video/exclude"
                elif ctgy == "https://vnexpress.net/bong-da/asian-cup-2019/binh-luan":
                    url = "https://vnexpress.net/the-thao/affcup2018/morenews/category_id/1004313/page/" + str(i) + "/catecode/binh-luan/exclude"
                elif ctgy == "https://vnexpress.net/the-thao/vleague-2018/tin-tuc#1004190":
                    url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004190/page/" + str(i) + "/exclude"
                elif ctgy == "https://vnexpress.net/the-thao/vleague-2018/anh#1004180":
                    url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004180/page/" + str(i) + "/exclude"
                elif ctgy == "https://vnexpress.net/the-thao/vleague-2018/video#1004181":
                    url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004181/page/" + str(i) + "/exclude"
                elif ctgy == "https://vnexpress.net/the-thao/vleague-2018/ben-le#1004182":
                    url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004182/page/" + str(i) + "/exclude"
                elif ctgy == "https://vnexpress.net/the-thao/vleague-2018/binh-luan#1004191":
                    url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004191/page/" + str(i) + "/exclude"
                else: continue
                request_database(url,arr)
def tuyen_sinh(url, arr):
    links = ["https://vnexpress.net/giao-duc/tuyen-sinh", "https://vnexpress.net/giao-duc/tuyen-sinh/cao-dang-trung-cap", "https://vnexpress.net/giao-duc/tuyen-sinh/thpt", "https://vnexpress.net/giao-duc/tuyen-sinh/thcs", "https://vnexpress.net/giao-duc/tuyen-sinh/tieu-hoc"]
    for ctg in links:
        print(ctg) 
        if ctg=="https://vnexpress.net/giao-duc/tuyen-sinh": continue
        else:   tuyen_sinh_links(ctg, arr)

def tuyen_sinh_links(url, arr):
    child_session = requests.session()
    child_webpage = child_session.get(url).text
    child_soup = BeautifulSoup(child_webpage, 'html.parser')
    child_main = child_soup.find(class_="col_left col_main")
    for child_ctg in child_main.find_all(class_="title_news"):
        arr.append(child_ctg.find('a').get('href').encode('utf-8'))
        print(child_ctg.find('a').get('href').encode('utf-8')) 
    next = child_soup.find('a', href=True, class_='next')
    if (next == None): continue_stmt
    else:
        link_next = "https://vnexpress.net" + next.get('href').encode('utf-8')
        print("L" + link_next) 
        tuyen_sinh_links(link_next, arr)
def start_up(arr):
    links = ["https://startup.vnexpress.net/tin-tuc/hanh-trinh-khoi-nghiep","https://startup.vnexpress.net/tin-tuc/xu-huong","https://startup.vnexpress.net/tin-tuc/y-tuong-moi","https://startup.vnexpress.net/tin-tuc/goc-chuyen-gia"]
    for ctg in links:
        if ctg == "https://startup.vnexpress.net/tin-tuc/hanh-trinh-khoi-nghiep":   maxpage = 32
        elif ctg == "https://startup.vnexpress.net/tin-tuc/xu-huong":               maxpage = 24
        elif ctg == "https://startup.vnexpress.net/tin-tuc/y-tuong-moi":            maxpage = 28
        else:                                                                       maxpage = 8
        for i in range(1, maxpage):
            if ctg == "https://startup.vnexpress.net/tin-tuc/hanh-trinh-khoi-nghiep":
                url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004062/page/" + str(i) + "/exclude?fbclid=IwAR1xEBfHsnzuRdSYIUiqOpeNKnMdrZm9P_I7A6pawEDmY79LqUae1yyrBSk"
            elif ctg == "https://startup.vnexpress.net/tin-tuc/xu-huong":
                url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004063/page/" + str(i) + "/exclude?fbclid=IwAR1xEBfHsnzuRdSYIUiqOpeNKnMdrZm9P_I7A6pawEDmY79LqUae1yyrBSk"
            elif ctg == "https://startup.vnexpress.net/tin-tuc/y-tuong-moi":
                url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004064/page/" + str(i) + "/exclude?fbclid=IwAR1xEBfHsnzuRdSYIUiqOpeNKnMdrZm9P_I7A6pawEDmY79LqUae1yyrBSk"
            else:
                url = "https://vnexpress.net/the-thao/seagame29/morenews/category_id/1004065/page/" + str(i) + "/exclude?fbclid=IwAR1xEBfHsnzuRdSYIUiqOpeNKnMdrZm9P_I7A6pawEDmY79LqUae1yyrBSk"
            request_database(url, arr)
def han_che_lam_dung_khang_sinh(url1, arr):
    for i in range(1, 6):
        url = "https://vnexpress.net/ajax/goc-nhin?category_id=1004195&page=" + str(i) + "&exclude=3&rule=2&fbclid=IwAR2bOd401tYEyyCjKvjlCbK1JXcVxMMq225hoGlFy00Ssud9NdhLnh6MnkM"
        request_database(url, arr)
def request_database(url, array):
    resp = requests.get(url=url)
    data = resp.json()
    for j in range(0, len(data['message'])):
        array.append(data['message'][j]['share_url'].encode('utf-8'))
        print(data['message'][j]['share_url']) 

def links(url,arr):
    global i
    session = requests.session()
    webpage = session.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')
    main_side = soup.find(class_='sidebar_1')
    if(main_side == None): continue_stmt
    else:
        sub_class = main_side.find_all(class_='title_news')
        for sub_c in sub_class:
            link = sub_c.find('a', href=True)
            print(link.get('href')) 
            arr.append(link.get('href').encode('utf-8'))
    next = soup.find('a', href=True, class_='next')
    if next == None: continue_stmt
    else:
        link_next = next.get('href').encode('utf-8')
        if("https://" not in next.get('href').encode('utf-8')):
            link_next = "https://vnexpress.net" + next.get('href').encode('utf-8')
        print("L" + link_next) 
        links(link_next,arr)
# if __name__ == '__main__':
#     categories()
    # url = "https://vnexpress.net/the-thao/p3"
    # links(url, the_thao)


