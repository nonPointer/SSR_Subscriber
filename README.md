# SSR_Subscriber

[English](#English) | [中文](#中文)

TODO:

+ [ ] Test connection intervals
+ [ ] Clean outdated config files

# English

SSR_Subscriber is a tool which based on Python3 to fetch latest configurations from your subscribe website and convert them into `config.json` files. It is used to deploy latest servers on routers or other devices without GUI.

## Feature

* Support multi subscriptions links
* Support keywords filter (such as save config files for those servers which remarks has a substring of `HK` or `Netflix`)



## Usage

1. Move `main.py` into the root directory of your local programs
2. Modify subscribe links
3. Execute and check if there are errors

# 中文

SSR_Subscriber 是一个基于 Python3 的小工具，用于自动从订阅服务器拉取服务器列表并存储至本地配置文件。它用于为路由等其它没有显示器的设施配置最新的服务器。

## 功能

* 支持多个订阅地址，为各订阅添加配置文件前缀
* 支持关键词筛选，例如筛选出名称含有 `HK` 或 `Netflix` 的服务器

## 使用方法

1. 将 `main.py` 移动至本地程序的根目录
2. 修改订阅地址
3. 执行并检查是否有异常输出