# coding=utf-8

from multiprocessing import Process,Queue
from multiprocessing.pool import Pool
from time import sleep
from sys import stdout

PRODUCTS=Queue()

def productor(product,out):
    sleep(3)
    print('put',product,out=out)
    PRODUCTS.put(product)

def consumer(out):
    while True:
        product=PRODUCTS.get()
        if product == None:
            print('consumer_thread exit')
            return
        print('get',product,out=out)
        sleep(1)

def main():
    proc=Process(target=consumer,args=(stdout,),name='consumer')
    proc.start()
    with Pool(5) as p:
        for i in range(5):
            print('---',i)
            p.apply_async(productor,(i,stdout))


if __name__ == '__main__':
    main()