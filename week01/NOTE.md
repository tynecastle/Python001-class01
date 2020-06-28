1. 编写简单爬虫
- 深入了解了python中requests、beautifulsoup、lxml、pandas模块功能的用法
- TCP协议、HTTP协议的基础知识
- xpath的使用方法
2. Scrapy爬虫框架核心组件
Scrapy框架的作用：实现了请求、跳转、下载、解析等流程，让开发者专注于业务逻辑。
- 引擎（Engine)：指挥Scrapy的大脑，协调其他组件工作
- 调度器（Scheduler）：将引擎发过来的请求压入队列，执行去重
- 下载器（Downloader）：下载爬到的数据，返回给引擎
- 爬虫器（Spiders）：指定要请求的内容；处理返回的数据
- 管道（Item Pipelines）：储存结果数据
- 下载器中间件：设置代理IP；request和response双向过滤
- 爬虫器中间件
通常情况下，开发者只需要修改其中的爬虫器和管道，其他组件无需修改，可以直接使用。
3. Scrapy框架使用
安装：pip install scrapy
创建项目：scrapy startproject demo
创建爬虫：scrapy genspider example example.com
运行爬虫：scrapy crawl example [--nolog]
4. Scrapy框架的特色功能
- debug
- 选择器
- 通过settings注册自定义属性
- 登录验证，并且在settings中将COOKIES_ENABLED置为True
- 在settings中配置动态请求延迟（AutoThrottle）
- 在settings中配置HTTP缓存（scrapy.extensions.httpcache.FilesystemCacheStorage）