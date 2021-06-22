# 一个短视频共享网站Demo



## 介绍

本项目为USTC CS 《数据库系统及应用》课程的大作业。本项目已经部署到[Heroku](https://www.heroku.com/)上，网址为https://hwzzlzlyh-short-video.herokuapp.com/ （仅作个人学习与测试使用！）

### 组员

[Weizhe Huang](https://github.com/weizhehuang0827)

[Yonghao Liang](https://github.com/yonghaoL)

[LiangZhuo Zhang](https://github.com/NSF-Nagisa)

## 使用方法

（注意：本项目在`python 3.9.4`环境下，用其他`python`版本可能会有问题）

首先使用`git clone`复制到本地

```
git clone git@github.com:weizhehuang0827/ShortVideo.git
```

`cd`切换到该项目主目录下，执行

```
python -m venv ll_env
```

即可在主目录下创建一个`python`虚拟环境，当前目录下就会有一个名为`ll_env`的目录，注意这里需要确认已经安装了`venv`库。

再在同一目录下执行该虚拟环境

**Windows**系统下为

```
ll_env\Scripts\activate
```

**Linux**系统下为

```
source ll_env/bin/activate
```

再下载项目依赖的包

```
pip install -r requirements.txt
```

再应用数据库的迁移

```
python manage.py migrate
```

之后就可以启动`django`服务器

```
python manage.py runserver
```

接下来就可以通过浏览器访问`http://localhost:8000/`来访问项目的web页面