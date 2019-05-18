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
        tables = pd.read_excel(self.base_path)
        return tables

    def son_name(self):
        '''
        保存每一个子表
        :return:
        '''
        tables = self.read_tables
        split_name = input('请输入你要按什么字段拆分')
        witer = pd.ExcelWriter(self.base_path)
        for name in set(tables[split_name]):
            df = tables[tables[split_name] == name]
            df.to_excel(excel_writer=witer, sheet_name=name, index=False)
            continue
        witer.save()

    def run(self):
        self.son_name()


def start():
    split_table = Split_Table()
    split_table.run()
    print('已成功拆分成多个子表')


if __name__ == '__main__':
    start()