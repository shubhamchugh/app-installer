# TOMYSELF

## applist.csv

我开始希望写一个功能相对多一点的脚本，比如在可以在多个APP中选择其中之一安装  
比如：`player1,player2`这种写法可以让用户选择安装player1或是player2，不仅仅是二选一，还应该要可以多选一  
但是有些时候我不能通过apk的包名知道这个apk到底是什么，如果有【多选1】的功能的话，就有可能会要对多个apk都加上描述  
比如：`player1,播放器1,player2,播放器2`  

**这太麻烦了，这会导致我花大量的时间去编辑applist.csv这个文件！**  
所以最后只留下一个功能，就是可以指定这个app在安装前是否询问  

为什么使用`pkg,comment`，而不是更简单的`pkg,flag`？  
因为大多数我要考虑是否需要安装的apk，都比较冷门，我不能从包名中知道它具体是哪一个

## 线程

5条下载线程+1条安装线程  
不把安装APP的任务提交给线程池，也不让同一条线程完成下载安装的任务，因为安装线程只能有一条  
adb只能一次安装一个APP，多条安装线程纯粹浪费时间

## 下载速度

简单测试，随便在酷安网上找了6个APP，5条线程比单线程快了5秒左右