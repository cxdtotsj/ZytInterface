import xlrd
from xlutils.copy import copy


class OperationExcel:

    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.filename = file_name
            self.sheet_id = sheet_id
        else:
            self.filename = "../dataconfig/protocommands.xls"
            self.sheet_id = 0
        self.data = self.get_data()

    # 获取sheet的内容
    def get_data(self):
        data = xlrd.open_workbook(self.filename)
        tables = data.sheets()[self.sheet_id]
        return tables

    # 获取单元格的行数
    def get_lines(self):
        tables = self.data
        return tables.nrows

    # 获取某个单元格的内容
    def get_cell_value(self, row, col):
        tables = self.data
        return tables.cell_value(row, col)

    # 写入数据
    def write_value(self, row, col, value):
        read_data = xlrd.open_workbook(self.filename)
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row, col, value)
        write_data.save(self.filename)


if __name__ == '__main__':
    opers = OperationExcel()
    print(opers.get_lines())
    print(opers.get_cell_value(2, 2))
    opers.write_value(2, 8, "test3")
