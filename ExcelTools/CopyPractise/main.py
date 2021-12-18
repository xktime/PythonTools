import openpyxl as op
import re
import pprint

'''
----------------------------------------实体类------------------------------
'''
class TargetEntity:
    def __init__(self):
        self.map = {}
        self.id = 0
        self.time = 0
        self.name = ""
        self.index = 0

'''
----------------------------------------method------------------------------
'''
def findMonthDatas(sheet, yearColumn, yearRow, year):
    entityMap = []
    month = 0
    for dataColumn in range(yearColumn, yearColumn + 12):
        month += 1
        monthMap = {}
        for row in range(yearRow + 1, sheet.max_row):
            index = sheet.cell(row, 1).value
            if index is None:
                continue
            id = sheet.cell(row, 2).value
            if id not in monthMap:
                entity = TargetEntity()
                entity.name = sheet.cell(row, 4).value
                entity.id = id
                entity.index = index
                entity.time = str(year) + str(month) + "月"
                monthMap[id] = entity
            entity = monthMap[id]
            projectName = sheet.cell(row, 5).value
            if projectName in entity.map and entity.map[projectName] > 0:
                continue
            dataValue = sheet.cell(row, dataColumn).value
            entity.map[projectName] = {True: 0, False: dataValue}[dataValue is None]
        entityMap.append(monthMap)
    return entityMap
'''
----------------------------------------main------------------------------
'''
sourceWb = op.load_workbook('E:\python\\files\9、管控格式-酉阳10.17王莉.xlsx')
sheetNames = sourceWb.sheetnames
entitys = {}##{sheetName, List<TargetEntity>}
for sheetName in sheetNames:
    sheet = sourceWb[sheetName]
    if re.match(r'.*税率*', str(sheetName)):
        continue
    max_row = sheet.max_row
    max_column = sheet.max_column
    for column in range(1, max_column):
        for row in range(1, max_row):
            cell = sheet.cell(row, column)
            year = cell.value
            if year is None:
                continue
            if re.match(r'(\d){4}年', str(year)) is None:
                continue
            entitys[year] = findMonthDatas(sheet, column, row, year)
    pprint.pprint(entitys)


# targetWb = op.Workbook()
# targetWb.save('.\\new.xlsx')