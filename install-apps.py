# coding=utf-8

import csv
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
from time import ctime
from argparse import ArgumentParser

from download import down

DEBUG = False

AppState = Enum('AppState', ('DOWNLOADING', 'DOWNLOADED',
                             'INSTALLING', 'INSTALLED', 'FAILED'))


class Apps():
    def read_csv(self,mode):
        apps = {}
        with open('applist.csv', encoding='utf-8') as file:
            for i in csv.reader(file):
                if len(i) > 1:
                    if mode == None and input('{}\n是否安装此App（y/n）：'.format(i[1])).lower() != 'y':
                        continue
                    elif mode == False:
                        continue
                apps[i[0]] = AppState.DOWNLOADING
        self._apps = apps
        self._condition = threading.Condition()

    def get_for_install(self):
        """
        获得一个状态为的DOWNLOADED的APP的包名
        """
        with self._condition:
            if not self.count(AppState.DOWNLOADING, AppState.DOWNLOADED):
                if DEBUG:
                    print('get_for_install', 'No DOWNLOADING or DOWNLOADED apps')
                return
            while not self.count(AppState.DOWNLOADED):
                if DEBUG:
                    print('get_for_install',
                          threading.current_thread().name, 'is waiting')
                self._condition.wait()

            for i in self._apps.items():
                if i[1] == AppState.DOWNLOADED:
                    self._apps[i[0]] = AppState.INSTALLING
                    return i[0]

    def count(self, *args):
        """
        统计某种状态的APP的数量
        """
        for arg in args:
            if not isinstance(arg, AppState):
                raise ValueError('arguments must be AppState type')
        with self._condition:
            i = 0
            for state in self._apps.values():
                if state in args:
                    i += 1
            return i

    def get_all(self):
        """
        返回包含所有app包名的迭代器
        """
        return self._apps.keys()

    def set_state(self, pkg, state):
        if not isinstance(state, AppState):
            raise ValueError(state)
        elif pkg not in self._apps.keys():
            raise ValueError(pkg+' is not in applist!')
        with self._condition:
            self._apps[pkg] = state
            if state == AppState.DOWNLOADED:
                if DEBUG:
                    print('notify!')
                self._condition.notify()

    def __init__(self,mode):
        self.read_csv(mode)

    def __str__(self):
        return str('\n'.join(['{pkg}: {state}'.format(pkg=i[0], state=i[1].name) for i in self._apps.items()]))


def install(apps):
    while True:
        pkg = apps.get_for_install()
        if not pkg:
            break
        try:
            print('开始安装', pkg)
            apps.set_state(pkg, AppState.INSTALLING)
            subprocess.check_output(
                'adb install {}.apk'.format(pkg), shell=True)
        except:
            print(pkg, '安装失败，因为↑')
            apps.set_state(pkg, AppState.FAILED)
        else:
            print('安装成功', pkg)
            apps.set_state(pkg, AppState.INSTALLED)


def get_args():
    parser = ArgumentParser(prog='install-apps',
                            description='Install apps for an Android phone')
    parser.add_argument('-o', dest='optional', action='store', choices={
                        'all', 'none', 'ask'}, default='ask', help='Whether to install optional apps')
    return parser.parse_args()

def main():
    args=get_args()
    mode=None
    if args.optional == 'all':
        mode=True
    elif args.optional == 'none':
        mode=False
    apps = Apps(mode)
    if DEBUG:
        print(apps)
    install_thread = threading.Thread(
        target=install, name='InstallThread', args=(apps,))
    install_thread.start()
    with ThreadPoolExecutor(max_workers=5, thread_name_prefix='DownThread') as executor:
        future_to_pkg = {executor.submit(
            down, pkg): pkg for pkg in apps.get_all()}
        for future in as_completed(future_to_pkg):
            if future.result():
                apps.set_state(future_to_pkg[future], AppState.DOWNLOADED)
            else:
                apps.set_state(future_to_pkg[future], AppState.FAILED)
    install_thread.join()
    if DEBUG:
        print(apps)


if __name__ == '__main__':
    print(ctime())
    main()
    print(ctime())
