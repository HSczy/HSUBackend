import multiprocessing
import os

'''
-c CONFIG    : CONFIG,配置文件的路径，通过配置文件启动；生产环境使用；

-b --bind ADDRESS   : ADDRESS，ip加端口，绑定运行的主机；

-w INT, --workers INT：用于处理工作进程的数量，为正整数，默认为1；

-k STRTING, --worker-class STRTING：要使用的工作模式，默认为sync异步，可以下载eventlet和gevent并指定

--threads INT：处理请求的工作线程数，使用指定数量的线程运行每个worker。为正整数，默认为1。

--worker-connections INT：最大客户端并发数量，默认情况下这个值为1000。

--backlog int：未决连接的最大数量，即等待服务的客户的数量。默认2048个，一般不修改；

-p FILE, --pid FILE：设置pid文件的文件名，如果不设置将不会创建pid文件


--access-logfile FILE   ：  要写入的访问日志目录

--access-logformat STRING：要写入的访问日志格式

--error-logfile FILE, --log-file FILE  ：  要写入错误日志的文件目录。

--log-level LEVEL   ：   错误日志输出等级。


--limit-request-line INT   ：  HTTP请求头的行数的最大大小，此参数用于限制HTTP请求行的允许大小，默认情况下，这个值为4094。值是0~8190的数字。

--limit-request-fields INT   ：  限制HTTP请求中请求头字段的数量。此字段用于限制请求头字段的数量以防止DDOS攻击，默认情况下，这个值为100，这个值不能超过32768

--limit-request-field-size INT  ：  限制HTTP请求中请求头的大小，默认情况下这个值为8190字节。值是一个整数或者0，当该值为0时，表示将对请求头大小不做限制


-t INT, --timeout INT：超过这么多秒后工作将被杀掉，并重新启动。一般设定为30秒；

--daemon： 是否以守护进程启动，默认false；

--chdir： 在加载应用程序之前切换目录；

--graceful-timeout INT：默认情况下，这个值为30，在超时(从接收到重启信号开始)之后仍然活着的工作将被强行杀死；一般使用默认；

--keep-alive INT：在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间。

--reload：默认为False。此设置用于开发，每当应用程序发生更改时，都会导致工作重新启动。

--spew：打印服务器执行过的每一条语句，默认False。此选择为原子性的，即要么全部打印，要么全部不打印；

--check-config   ：显示现在的配置，默认值为False，即显示。

-e ENV, --env ENV： 设置环境变量；
'''

bind = '0.0.0.0:8080'
# workers = multiprocessing.cpu_count() * 2 + 1  # 进程数
# threads = 2  # 指定每个进程开启的线程数
timeout = 86400  # debug 使用，生产环境取消
if not os.path.exists('./Logs/gunicorn'):
    os.mkdir('./Logs/gunicorn')
accesslog = './Logs/gunicorn/access_log'
errorlog = './Logs/gunicorn/error_log'
access_log_format = '%(t)s %(h)s "%(r)s" %(s)s %(L)s %(m)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置

'''
h	remote address
l	'-'
u	user name
t	date of the request
r	status line (e.g. GET / HTTP/1.1)
m	request method
U	URL path without query string
q	query string
H	protocol
s	status
B	response length
b	response length or '-' (CLF format)
f	referer
a	user agent
T	request time in seconds
M	request time in milliseconds
D	request time in microseconds
L	request time in decimal seconds
p	process ID
{header}i	request header
{header}o	response header
{variable}e	environment variable
'''
