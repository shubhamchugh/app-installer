# app-installer

从applist.csv中读取需要下载的APP，然后从[酷安网](https://www.coolapk.com/)/[apkpure](https://apkpure.com/cn/)下载并安装到手机

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

`install-apps.py -o {ask,none,all}`  

- ask：默认选项，对于一些可选的apk，询问用户是否安装  
- none：所有可选的apk全都不安装
- all：所有可选的apk全都安装

## TODO

- [ ] setup.py还没写
- [ ] 下载的apk不会自动删除，加一个选项
- [ ] 加一个只下载不安装的选项