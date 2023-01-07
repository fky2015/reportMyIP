# Report-My-IP

一个 Client-Server 式的远程查看动态分配 IP 的程序。

**这是一个玩具性质的项目，代码非常原始，仅提倡供学习交流使用。**

## 使用方式

`pipenv install`

然后修改 `clientSide` 的配置文件，并分别启动 `clientSide` （可以定时执行） 与 `serverSide`。

## 针对什么问题

比如个人电脑会经常改变 IP。如果有一次在外面想远程登录电脑，就需要提前记好 IP，但是如果利用一台固定的服务器，就可以查看到最新的 IP。

## 项目架构

### client

每个需要获取 IP 的主机
简单的脚本实现，只支持 Linux。

### server

一台可访问的服务器。

### 采用 RESTFUL 设计

```url
GET /hosts

GET /my_ip?hostname=MY_HOST_NAME

PUT /my_ip?hostname=MY_HOST_NAME
```
