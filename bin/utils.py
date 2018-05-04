#!/usr/bin/env python
#coding=utf-8
import os

import sys

import fabric
from fabric.api import *
from fabric.colors import green
from fabric.contrib.console import confirm
reload(sys)
sys.setdefaultencoding("utf-8")
import time
#项目编译，一个命令列表
def compile(cmdList):
    print green("开始执行命令列表")
    for cmd in cmdList:
        res=local(cmd)
        print green("执行命令:"+cmd+",返回:"+res)
    print green("命令列表执行完成")
#执行SLB
def setSlb(slbServer,slb,weight):
    host=env.host
    #当前阿里云的server id
    server=slbServer.get(host)
    #print server
    print green("对slb"+slb+",其中server:"+server+",设置为:"+str(weight))
    res=local("pwd")
    res=local("aliyuncli slb SetBackendServers --BackendServers --LoadBalancerId %s --BackendServers  \"[{'ServerId':'%s','Weight':'%s'}]\"" % (slb,server, weight))
#上传接口
def upload(source,target):
    print green("上传文件:"+source+"到:"+target)
    fileName = os.path.basename(source)
    if fabric.contrib.files.exists(os.path.join(target, fileName)):
        with settings(warn_only=True):
            print green("删除:"+os.path.join(target, fileName));
            run("rm -rf " + os.path.join(target, fileName))
    with settings(warn_only=True):
        result = put(source, target)
    if result.failed and not confirm("put file failed, Continue[Y/N]?"):
        abort("终止任务")
#远程打包接口
def zip(online):
    fileName = os.path.split(online)[1]
    print green("打包文件:"+fileName)
    with cd(online):
         run("set -m;pwd;zip -r %s ./*" %(fileName))
#解压缩
def unzip(online):
    fileName = os.path.split(online)[1]
    print green("解压缩文件:"+fileName)
    run("set -m;pwd;unzip -o %s.zip -d %s" %(fileName,online))
#下载接口
@runs_once
def download(online,localPath):
    fileName1 = os.path.split(online)[1]
    fileName = '%s%s' %(fileName1,'.zip')
    tmpfile1 = os.path.join(online, fileName1)
    tmpfile = '%s%s' %(tmpfile1,'.zip')
    print green("下载文件:"+fileName+"到:"+localPath)
    tmp = os.path.join(localPath,fileName)
    dateStr=time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    if os.path.exists(tmp):
        with lcd(localPath):
            local("mkdir %s;mv %s %s" %(dateStr,fileName,dateStr))
    with settings(warn_only=True):
        result = get(tmpfile, localPath)
    if result.failed and not confirm("put file failed, Continue[Y/N]?"):
        abort("终止任务")
    run ("rm -f %s" %(tmpfile)) 
#关闭进程
def stopProcess(aport):
    with settings(warn_only=True):
        #print aport
        #processStr=run("set -m;jps | grep -v Jps | awk '{print $1}'");
        processStr=run("set -m;lsof -i :%s | sed -n '2p' | awk '{print $2}'" %(aport));
        processList=processStr.split("\n")
        for process in processList:
            with settings(warn_only=True):
                run("set -m;kill -9 "+process)
#启动进程
def runCmd(cmd="pwd",setm=True):
    with settings(warn_only=True):
        if setm:
            run("set -m;"+cmd)
        else:
            run(cmd)
