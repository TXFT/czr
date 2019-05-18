import pandas as pd
import os

class Split_Table:
    '''
    拆分excel中的多个子工作表为单独的工作薄
    '''
    base_path = input('请输入你要拆分文件的路径：')

    @property
    def file_path(self):
        '''文件的路径'''
        filepath, tempfilename = os.path.split(self.base_path)
        return filepath

    @property
    def read_tables(self):
        '''
        缓存文件到内存
        :return:
        '''
        tablepath = self.base_path
        tables = pd.read_excel(tablepath, None)
        return tables

    def son_name(self):
        '''
        保存每一个子表
        :return:
        '''
        tables = self.read_tables
        names = tables.keys()
        n = int(input('请输入读取文件的表头是从第几行开始：'))
        for name in names:
            tempsheet = pd.read_excel(self.base_path, sheet_name=name, header=(n, ))
            tempsheet.to_excel(self.file_path + '\\' + name + '.xlsx', sheet_name=name, index=False)

    def run(self):
        self.son_name()


def start():
    split_table = Split_Table()
    split_table.run()
    print('已成功拆分到打开文件的文件夹中')


if __name__ == '__main__':
    start()