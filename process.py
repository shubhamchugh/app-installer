# coding=utf-8

from multiprocessing import Process,Queue,Pool
from time import sleep

INSTALLED_APPS=Queue()

def productor(product):
    print('productor',product)
    sleep(3)
    print('put',product)
    INSTALLED_APPS.put(product)

def consumer():
    print('consumer')
    while True:
        product=INSTALLED_APPS.get()
        if product == None:
            print('consumer_thread exit')
            return
        print('get',product)
        sleep(1)

def main():
    proc=Process(target=consumer,name='consumer')
    proc.start()
    pool=Pool(5)
    for i in range(5):
        print('---',i)
        pool.apply_async(productor,(i,))
    pool.close()
    pool.join()
    INSTALLED_APPS.put(None)
    proc.join()

if __name__ == '__main__':
    main()
