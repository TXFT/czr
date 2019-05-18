import win32api, win32con
import time
from vc_code import VK_CODE


class My_Win:
    def cursor_point(self):
        """
         获取当前鼠标位置
        """
        pos = win32api.GetCursorPos()
        return int(pos[0]), int(pos[1])

    def mouse_left_click(self, new_x=None, new_y=None, times=2):
        """
        鼠标左击事件
        :param new_x: 新移动的坐标x轴坐标
        :param new_y: 新移动的坐标y轴坐标1506240215
        :param times: 点击次数
        """
        self.mouse_move(new_x, new_y)
        time.sleep(0.05)
        while times:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            times -= 1

    def mouse_right_click(self, new_x=None, new_y=None):
        """
        鼠标右击事件
        :param new_x: 新移动的坐标x轴坐标
        :param new_y: 新移动的坐标y轴坐标
        """
        self.mouse_move(new_x, new_y)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def mouse_move(self, new_x, new_y):
        '''
        鼠标移动像素大小
        :param new_x:
        :param new_y:
        :return:
        '''
        if new_y is not None and new_x is not None:
            point = (new_x, new_y)
            win32api.SetCursorPos(point)
            self.x = new_x
            self.y = new_y

    def key_input(self, input_words=""):
        '''
        键盘输入值
        :param input_words:
        :return:
        '''
        for word in input_words:
            win32api.keybd_event(VK_CODE[word], 0, 0, 0)
            win32api.keybd_event(VK_CODE[word], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)


if __name__ == '__main__':

    for i in range(16, 31):
        # 交易开始时间
        test = My_Win()
        test.cursor_point()
        test.mouse_move(301, 141)
        test.mouse_left_click(times=1)
        test.key_input(str(i))

        # 交易结束时间
        test = My_Win()
        test.cursor_point()
        test.mouse_move(597, 141)
        test.mouse_left_click(times=1)
        test.key_input(str(i))

        # 点击刷新初数据

        test = My_Win()
        test.cursor_point()
        test.mouse_move(213, 106)
        test.mouse_left_click(times=1)

        # 等待1秒
        time.sleep(20)

        # 导出数据
        test = My_Win()
        test.cursor_point()
        test.mouse_move(947, 302)
        test.mouse_right_click()
        time.sleep(0.1)
        test.mouse_left_click(new_x=947+70, new_y=302+15,times=1)
        time.sleep(1)
        test.key_input(str(i))
        time.sleep(0.1)

        # 保存数据
        win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)

        win32api.keybd_event(VK_CODE['enter'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['enter'], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(2)