import openpyxl as op
import time
from elasticsearch import Elasticsearch
import xml.dom.minidom as xml

ROLE_ID_COLUMN = 1
ROLE_NAME_COLUMN = 2
LEVEL_COLUMN = 3
GUIDE_ID_COLUMN = 4
CHAPTER_COLUMN = 5
LOGIN_TIME_COLUMN = 6


def get_es_data(index):
    dom = xml.parse('config.xml')
    root = dom.documentElement
    adress = root.getElementsByTagName('adress')[0].firstChild.data
    username = root.getElementsByTagName('username')[0].firstChild.data
    password = root.getElementsByTagName('password')[0].firstChild.data
    es = Elasticsearch(['http://' + adress], http_auth=(username, password))
    count = es.count(index=index)["count"]
    fromIndex = 0
    size = 1000
    results = []
    while fromIndex < count:
        body = {
            "_source": ["lastLoginTime", "chapter", "guideId", "level", "roleId", "roleName"],
            "query": {
                "match_all": {
                },
            },
            "from": fromIndex,
            "size": size,
            "track_total_hits": "true"
        }
        fromIndex += size
        datas = es.search(index=index, body=body)
        results.extend(datas['hits']['hits'])
    return results


def get_filter_data(crossTime, index):
    beforeMap = {}  ## <roleId, times>
    afterMap = {}
    for result in get_es_data(index):
        source = result["_source"]
        roleId = source["roleId"]
        formatTime = time.strptime(result["_source"]["lastLoginTime"], '%m/%d/%Y %H:%M:%S')
        if formatTime < crossTime:
            if beforeMap.__contains__(roleId):
                if time.strptime(beforeMap[roleId]['lastLoginTime'], '%m/%d/%Y %H:%M:%S') < formatTime:
                    beforeMap[roleId] = source
            else:
                beforeMap[roleId] = source
        else:
            afterMap[roleId] = source
    result = []
    for info in beforeMap.values():
        roleId = info["roleId"]
        if afterMap.__contains__(roleId):
            continue
        result.append(info)
    return result


def export_to_excel(time, index):
    wb = op.Workbook()
    sheet = wb.create_sheet("行为统计")
    sheet.cell(1, ROLE_ID_COLUMN).value = '玩家id'
    sheet.cell(1, ROLE_NAME_COLUMN).value = '玩家名字'
    sheet.cell(1, LEVEL_COLUMN).value = '等级'
    sheet.cell(1, GUIDE_ID_COLUMN).value = '引导id'
    sheet.cell(1, CHAPTER_COLUMN).value = '关卡'
    sheet.cell(1, LOGIN_TIME_COLUMN).value = '最后登录时间'

    row = 2
    for info in get_filter_data(time, index):
        sheet.cell(row, ROLE_ID_COLUMN).value = str(info["roleId"])
        sheet.cell(row, ROLE_NAME_COLUMN).value = info["roleName"]
        sheet.cell(row, LEVEL_COLUMN).value = info["level"]
        sheet.cell(row, GUIDE_ID_COLUMN).value = str(info["guideId"])
        sheet.cell(row, CHAPTER_COLUMN).value = info["chapter"]
        sheet.cell(row, LOGIN_TIME_COLUMN).value = info["lastLoginTime"]
        row += 1

    wb.save("./result.xlsx")


print("请输入需要查询的索引")
index = input()
print("请输入需要查询【年/月/日 时：分：秒】之后未登陆过的玩家")
datetime = input()
try:
    datetime = time.strptime(datetime, '%Y/%m/%d %H:%M:%S')
except:
    print("时间格式输入错误，格式应为 年/月/日 时：分：秒")
else:
    export_to_excel(datetime, index)
