# celery_demo
利用Celery 实现远程woker

# 需求
在我现在的工作当中，我需要实现一种机制，就是服务端来分发任务，worker端来干活。在我看了很多的文章之后，发现Celery这个东西还是相当不错的。  
自己的队列。自已可以处理任务分发的工作。

# package依赖
1. gevent 实现多进程访问
2. Flask
3. Celery
以上三个为主要的依赖包。备注： 我用的是 py2.7

# 代码讲解
## app.py
### Send two numbers to add
@app.route('/add/<int:param1>/<int:param2>')  
def add(param1,param2):  
    task = celery.send_task('mytasks.add', args=[param1, param2])    
    return task.id  
在Flask当中增加一个请求，这个请求里面有两个参数。  
其次，最关健的一句话，celery.send_task()是把任务发给一个叫做mytasks.add的worker  
发送成功以后，会返回一个以uuid形式的job ID

### Check the status of the task with the id found in the add function
@app.route('/check/<string:id>')  
def check_task(id):   
    res = celery.AsyncResult(id)  
    return res.state if res.state==states.PENDING else str(res.result)  
这个接口是用来检查当前Job ID的状态。如果是执行当中，返回PENDING，如果有结果了，直接返回结果。  

## tasks.py
### The name parameter is the key here
@celery.task(name='mytasks.add')  
def add(x, y):  
    time.sleep(5) # lets sleep for a while before doing the gigantic addition task!    
    return x + y  
 最关健就是这里。 add在主程序里面调用了接口以后，会通过send_task给一个叫做'mytasks.add'的worker.   
 那么这个worker就在这里。他完成加法操作以后，会直接给主程序app.py返回结果
 
# 部署和启动
在我的程序里面，我用的是redis做为我的broker。配置很简单，大家在网上找一份ubuntu或者windows的配置，照着做就可以了  
 
## A机器（服务端）  
首先在A机器上面部署好，然后直接启动app.py  
如果所有的package都安装完成以后，flask应该会告诉你程序启动成功。  
默认访问 http://127.0.0.1:5000
 
## B机器（worker端）
把程序一模一样的copy到B机器去。   
启动worker命令：    
celery -A tasks worker --loglevel=info  

备注：   
1. 你可以启动多个worker端，在一台机器上面  
2. 在B机器上面你不用启动app.py主程序

## 调用 
这个时候 你可以写一个测试调用的py或者java什么的，哪个语言熟悉就用哪个语言来写。循环调用主程序里面的/add的那个接口。  
这个时候 你会看到，celery帮你做分发，并且所有的worker都启动开始干活了




 
 
 
 






