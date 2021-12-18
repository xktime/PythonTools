import pprint
import re

import openpyxl as op

'''
----------------------------------------实体类------------------------------
'''


class TargetEntity:
    def __init__(self):
        self.map = {}
        self.companyId = 0
        self.time = 0
        self.companyName = ""
        self.index = 0


'''
----------------------------------------method------------------------------
'''


def findMonthDatas(entitys, sheet, yearColumn, yearRow):
    month = 0
    year = sheet.cell(yearRow, yearColumn).value
    if year not in entitys:
        monthMap = {}
        entitys[year] = monthMap
    monthMap = entitys[year]
    for dataColumn in range(yearColumn, yearColumn + 12):
        month += 1
        if month not in monthMap:
            dataMap = {}##map<companyId, List<TargetEntity>>
            monthMap[month] = dataMap
        dataMap = monthMap[month]
        for row in range(yearRow + 1, sheet.max_row):
            index = sheet.cell(row, 1).value
            if index is None:
                continue
            companyId = sheet.cell(row, 2).value
            if companyId not in dataMap:
                entity = TargetEntity()
                entity.companyName = sheet.cell(row, 4).value
                entity.companyId = companyId
                entity.index = index
                entity.time = str(year) + str(month) + "月"
                dataMap[companyId] = entity
            entity = dataMap[companyId]
            projectName = sheet.cell(row, 5).value
            if projectName in entity.map and entity.map[projectName] > 0:
                continue
            dataValue = sheet.cell(row, dataColumn).value
            entity.map[projectName] = {True: 0, False: dataValue}[dataValue is None]


##return map<year, map<month, map<companyId, TargetEntity>>
def getEntitys(sourcePath):
    sourceWb = op.load_workbook(sourcePath)
    sheetNames = sourceWb.sheetnames
    entitys = {}
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
                findMonthDatas(entitys, sheet, column, row)
    return entitys


'''
----------------------------------------main------------------------------
'''
entitys = getEntitys('./testData.xlsx')
pprint.pprint(entitys)

# targetWb = op.Workbook()
# targetWb.save('.\\new.xlsx')
