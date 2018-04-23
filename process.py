# coding=utf-8

from multiprocessing import Process,Queue,Pool
from time import sleep

def productor(product,downloaded_apps):
    print('productor',product)
    sleep(3)
    print('put',product)
    downloaded_apps.put(product)

def consumer(downloaded_apps):
    print('consumer')
    while True:
        product=downloaded_apps.get()
        if product == None:
            print('consumer_thread exit')
            return
        print('get',product)
        sleep(1)

def main():
    downloaded_apps=Queue()
    proc=Process(target=consumer,args=(downloaded_apps,),name='consumer')
    proc.start()
    pool=Pool(5)
    for i in range(5):
        print('---',i)
        pool.apply_async(productor,(i,downloaded_apps))
    pool.close()
    pool.join()
    downloaded_apps.put(None)
    proc.join()

if __name__ == '__main__':
    main()
