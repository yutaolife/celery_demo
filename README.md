# celery_demo
利用Celery 实现远程woker

# 需求
在我现在的工作当中，我需要实现一种机制，就是服务端来分发任务，worker端来干活。在我看了很多的文章之后，发现Celery这个东西还是相当不错的。  
自己的队列。自已可以处理任务分发的工作。

#package依赖
1. gevent 实现多进程访问
2. Flask
3. Celery
以上三个为主要的依赖包。备注： 我用的是 py2.7

#代码讲解


