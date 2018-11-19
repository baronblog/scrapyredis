## Scrapy 分布式爬虫

### 实现功能点如下：
* 使用Redis代替Scrapy默认调度器组成分布式爬虫
* 使用xpath抽取相关数据
* 针对网站反爬，重写Scrapy的管道组件(pipeline)，随机更换user_agent/referral/ip
* 使用Twisted框架的adbapi创建连接池存储数据到Mysql


实现思路图如下：
* 开始从自己编写的业务爬虫开始，发送request请求到engine，spider主要是确定要下载的网页，engine主要是负责所有组件之间的数据流
* 之后engine把request请求发送给scheduler，并将它们排入队列，之后engine从scheduler中一个个开始拉取request请求，发送给downloader，途中会经过下载中间件
* 下载完成之后便返回，途中还会经过中间件，中间件会把获取到的结果发给engine，engine然后会给spider发送一个response，在这途中会经过中间件
* spider处理后经过中间件把处理后的数据和下一个要请求的发送给engine，引擎将处理后的数据发给管道(包括item和piplines)，完成一次循环过程，之后engine又再从scheduler

分布式爬虫思路：
* 主要是把之前默认的scheduler改为用redis代替即可