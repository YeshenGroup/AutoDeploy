#!/usr/bin/env python
#coding=utf-8
import ConfigParser
import json
import sys
import os
from datetime import time
from fabric.colors import green, red
from fabric.state import env
import utils
from fabric.api import *
reload(sys)
sys.setdefaultencoding("utf-8")
#读取项目配置
@task
def set(config):
    cf = ConfigParser.ConfigParser()
    cf.read(config)
    project="project"
    env.gateway = cf.get(project,"gateway")
    env.key_filename=cf.get(project,"key_filename")
    env.hosts=json.loads(cf.get(project,"hosts"))
    env.passwords=json.loads(cf.get(project,"passwords"))
    env.exclude_hosts=json.loads(cf.get(project,"exclude_hosts"))
    env.slbList=json.loads(cf.get(project,"slb"))
    env.slbServer=json.loads(cf.get(project,"server"))
    env.aport = cf.get(project, "aport")
    env.source=cf.get(project,"source")
    env.target=cf.get(project, "target")
    env.online=cf.get(project, "online")
    env.localPath=cf.get(project, "localPath")
    env.start_process = cf.get(project, "start_process")
    env.monitor_url= cf.get(project, "monitor_url")
    env.sleep_time = cf.get(project, "sleep_time")
    #env.cmdlist=json.load(cf.get(project,"cmd"))

#灰度部署
@task
def huidu_deploy(machine=None):
    print green("当前机器:"+env.host)
    #如果指定机器,那就只上着一个
    if machine and not machine==env.host:
        return
    #关闭slb
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,0)
    utils.runCmd("sleep 5")
    #备份
    #utils.zip(env.online)
    #utils.download(env.online,env.localPath)
    #上传
    utils.upload(env.source,env.target)
    #杀掉进程
    utils.stopProcess(env.aport)
    utils.runCmd("sleep 10")
    #解压缩
    utils.unzip(env.online)
    #开始进程
    utils.runCmd(env.start_process)
    #sleep 多少秒
    utils.runCmd("sleep "+env.sleep_time)
    #监控进程
    run(env.monitor_url)
#灰度部署
@task
def huidu_deploy_none_restart(machine=None):
    print green("当前机器:"+env.host)
    #如果指定机器,那就只上着一个
    if machine and not machine==env.host:
        return
    #关闭slb
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,0)
    utils.runCmd("sleep 5")
    #备份
    # utils.zip(env.online)
    # utils.download(env.online,env.localPath)
    #上传
    utils.upload(env.source,env.target)
    #杀掉进程
    # utils.stopProcess(env.aport)
    # utils.runCmd("sleep 10")
    #解压缩
    utils.unzip(env.online)
    #开始进程
    # utils.runCmd(env.start_process)
    #sleep 多少秒
    # utils.runCmd("sleep "+env.sleep_time)
    #监控进程
    run(env.monitor_url)
#部署
@task
def deploy(machine=None):
    print green("当前机器:"+env.host)
    #如果指定机器,那就只上着一个
    if machine and not machine==env.host:
        return
    #关闭slb
    #print env.host
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,0)
    utils.runCmd("sleep 5")
    #备份
    utils.zip(env.online)
    utils.download(env.online,env.localPath)
    #上传
    utils.upload(env.source,env.target)
    #杀掉进程
    utils.stopProcess(env.aport)
    utils.runCmd("sleep 10")
    #解压缩
    utils.unzip(env.online)
    #开始进程
    utils.runCmd(env.start_process)
    #sleep 多少秒
    utils.runCmd("sleep "+env.sleep_time)
    #监控进程
    run(env.monitor_url)
    #上线slb
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,100)

#灰度部署
@task
def deploy_none_restart(machine=None):
    print green("当前机器:"+env.host)
    #如果指定机器,那就只上着一个
    if machine and not machine==env.host:
        return
    #关闭slb
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,0)
    utils.runCmd("sleep 5")
    #备份
    utils.zip(env.online)
    utils.download(env.online,env.localPath)
    #上传
    utils.upload(env.source,env.target)
    #杀掉进程
    # utils.stopProcess(env.aport)
    # utils.runCmd("sleep 10")
    #解压缩
    utils.unzip(env.online)
    #开始进程
    # utils.runCmd(env.start_process)
    #sleep 多少秒
    # utils.runCmd("sleep "+env.sleep_time)
    #监控进程
    run(env.monitor_url)
    #上线slb
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,100)


#设置slb
@task
def setSlb(machine=None,weight=None):
    print green("当前机器:"+env.host)
    if not machine or not weight:
        abort("机器和权重不能为空")
    #如果指定机器,那就只上着一个
    if not machine==env.host:
        return
    #关闭slb
    for slb in env.slbList:
        utils.setSlb(env.slbServer,slb,weight)

#上传文件
@task
def upload(source=None,target=None,machine=None):
    print green("当前机器:"+env.host)
    if not machine or not source or not target:
        abort("机器、源路径、目标路径不能为空")
    if machine and not machine==env.host:
        return
    utils.upload(source,target)
#压缩文件
@task
def zip(online=None,machine=None):
    if not machine or not online:
        abort("机器、远程路径不能为空")
    print green("当前机器:"+env.host)
    if machine and not machine==env.host:
        return
    utils.zip(online)
#下载文件
@task
def download(online=None,localPath=None,machine=None):
    if not machine or not online or not localPath:
        abort("机器、远程路径、本地目标路径不能为空")
    print green("当前机器:"+env.host)
    if machine and not machine==env.host:
        return
    utils.download(online,localPath)

@task
def stopProcess(aport=None,machine=None):
    if not machine or not aport:
        abort("机器、aport不能为空")
    print green("当前机器:"+env.host)
    if machine and not machine==env.host:
        return
    utils.stopProcess(aport)

#解压缩
@task
def unzip(online=None,machine=None):
    if not machine or not online:
        abort("机器、online路径不能为空")
    print green("当前机器:"+env.host)
    if machine and not machine==env.host:
        return
    utils.unzip(online)

#执行命令
@task
def runCmd(cmd,machine=None):
    if not machine or not cmd:
        abort("机器、cmd不能为空")
    print green("当前机器:"+env.host)
    if machine and not machine==env.host:
        return
    utils.runCmd(cmd)
