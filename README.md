# app-installer

从applist.csv中读取需要下载的APP，然后从 [酷安网](https://www.coolapk.com/) 或 [apkpure](https://apkpure.com/cn/) 下载并安装到手机  

写这个脚本是因为国内的同步助手的功能不能同步我的部分App，比如影梭在国内的应用市场就无法找到  
而酷安网+apkpure的组合几乎能下载到所有我需要的App

还有一个问题无法解决，国内手机用adb安装App时，需要在手机屏幕点击【确认】按钮，所以这个脚本还是无法做到全自动

## applist.csv

格式如下

`com.tencent.mm`  
`com.tencent.qqlite,QQ轻聊版`  

英文逗号作为分隔符，第一个字段是apk包名，第二个是描述  
第二个字段是可选的，如果添加了第二个字段那在默认情况下脚本会询问用户是否要安装这个apk  
我一般在第二个字段只写apk的名称，当然也可以写其它的  

## 使用方法

请保证有且仅有一台Android手机连接到adb  

```bash
$ adb devices
List of devices attached
XXXXXXX        device
```

请保证当前目录中有applist.csv这个文件

`install-apps -o {ask,none,all} -d -r`  

`-o`：  

- ask：默认选项，对于一些可选的apk，询问用户是否安装
- none：所有可选的apk全都不安装
- all：所有可选的apk全都安装

`-d`：仅下载，不安装  
`-r`：删除安装成功的apk文件

## TODO

- [x] setup.py还没写
- [x] 下载的apk不会自动删除，加一个选项
- [x] 加一个只下载不安装的选项
- [x] 如果手机中已经安装了applist.csv中记录的apk，则无需再下载
- [] 对于下载中断的apk文件，发起第二次下载请求

## NOT TODO

- 不会去判断当前环境是否安装有adb
- 不会去判断当前目录是否有applist.csv文件