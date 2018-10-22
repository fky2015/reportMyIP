# Report-My-IP

一个clint-server式的远程查看动态分配ip的程序。

## 针对什么问题

比如个人电脑会经常改变ip。如果有一次在外面想远程登录电脑，就需要提前记好ip，但是如果利用一台固定的服务器，就可以查看到最新的ip。

## 项目架构

### client

每个需要获取ip的主机
简单的脚本实现

### server

一台可访问的服务器
`golang`实现http server

### 采用rest设计

```url
GET /hosts

GET /my_ip?hostname=MY_HOST_NAME

PUT /my_ip?hostname=MY_HOST_NAME
```
