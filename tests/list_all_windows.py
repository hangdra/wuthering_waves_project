# @Author  : liuha
# @Time    : 2026/7/13 04:01
# @File    : list_all_windows.py

import win32con
import win32gui
import win32ui, win32api
import time

def list_window_names():
    def winEnumHandler(hwnd_id, ctx):
        if win32gui.IsWindowVisible(hwnd_id):
            print(hex(hwnd_id), '"' + win32gui.GetWindowText(hwnd_id) + '"')
            list_inner_windows(hwnd_id)

    win32gui.EnumWindows(winEnumHandler, None)
    print("------------over------------------")


def list_inner_windows(whndl):
    def callback(hwnd_id, hwnds):
        if win32gui.IsWindowVisible(hwnd_id) and win32gui.IsWindowEnabled(hwnd_id):
            hwnds[win32gui.GetClassName(hwnd_id)] = hwnd_id
            return True

    hwnds = {}
    win32gui.EnumChildWindows(whndl, callback, hwnds)
    if hwnds:
        print(str(whndl), "child", hwnds)

    print("------------over------------------")
    return hwnds

list_window_names()
