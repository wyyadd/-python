# 东南大学每日自动健康打卡（基于python selenium)

一. 代码借鉴于https://gitee.com/yindaheng98/AutoLogin

简化了好多， 加了文件流读账号密码，删去了日志功能.......

二. 如何运行？

要求： 一个云服务器， 推荐linux版的， windows的也行

1\. 首先在服务器上安装chrome和chromedriver（必须）

2\. 此为分支

简化版： 直接下载我配置好的包， 修改包里面的user.txt就行，
把包上传到服务器上（我的服务器为ubuntu系统），
运行DailyReport程序就行（用nohup后台运行）

复杂版： 自定义修改代码， 然后用pyinstaller生成可执行程序， 上传服务器，
再运行即可。

一些注意事项：

1\. 服务器运行程序的时候不要用root身份（大坑 哭～）

2\. 用pyinstaller生成可执行程序不要用 ---onefile 或 -F，
即只生成一个文件，要不然读取不了user.txt

3\. 我本人配置好的包 链接: https://pan.baidu.com/s/1jqJuLXorLESimmeJFCS2BQ 提取码: nxqr
