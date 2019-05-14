import pandas as pd
import os


class Split_Table:
    '''
    拆分excel中的多个子工作表为单独的工作薄
    '''
    base_path = input('请输入你要拆分文件的路径：')
    split_name = input('请输入你要按什么字段拆分：')
    folder_name = input('请输入你想保存在哪个文件夹里面：')

    @property
    def file_path(self):
        '''文件的路径'''
        filepath, tempfilename = os.path.split(self.base_path)
        return filepath

    @property
    def read_tables(self):
        '''
        缓存文件到内存
        :return: tables
        '''
        tables = pd.read_excel(self.base_path)
        return tables

    def son_name(self):
        '''
        保存每一个子表
        :return: self.file_path + '\\%s\\' % self.folder_name
        '''
        tables = self.read_tables

        for name in set(tables[self.split_name]):
            df = tables[tables[self.split_name] == name]
            try:
                df['消耗率'] = df['消耗率'].apply(lambda x: format(x, '.2%'))
                df.to_excel(self.file_path + '\\%s\\' % self.folder_name + name + '.xlsx', sheet_name=name, index=False)
            except KeyError:
                df.to_excel(self.file_path + '\\%s\\' % self.folder_name + name + '.xlsx', sheet_name=name, index=False)
        return  self.file_path + '\\%s\\' % self.folder_name


    def run(self):
        self.son_name()


def start():
    split_table = Split_Table()
    split_table.run()
    print('已成功拆分到打开文件的文件夹中')

if __name__ == '__main__':
    start()