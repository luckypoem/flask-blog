# 利用flask框架制的个人博
## 基本功能
实现文章分类，支持在线markdow语言书写博客。ps:兼容python3.5和python2.7。
## 使用方法
下载源码后
```cmd
pip install -r requirements.txt
```
安装所需的库。
```python
python manage.py init_data
```
初始化数据库信息。
```python
python manage.py runserver
```
启动本地服务。  
输入[127.0.0.1:5000/woodenrobot/login]()入登录页面。  
默认账号和密码为：woodenrobo  123  
登陆后可对文章进行新建、修改和删除。  
项目演示：[https://woodenrobot.herokuapp.com/]()
