# dailyfresh
从头完成一个完整天天生鲜电商项目后端
有些东西久了不做会生疏，再从头完成一个生鲜电商项目，后期尽可能增加更复杂更流行的功能。

### 初始化配置完成：
- django-admin startproject dailyfresh 创建项目
- 创建apps目录，将app归纳在该目录中便于管理
- sys.path.insert(0,os.path.join(BASE_DIR,'apps'))添加apps为导包路径
- python manage.py startapp user 创建app
- include两级url路由及注册
- 模型类创建及迁移，AUTH_USER_MODEL指定认证系统使用的模型类
- 修改默认数据库为mysql
- 增加Redis缓存CACHES设置
- 添加session认证设置
- 修改语言及时区
- 添加logging日志设置
- 创建静态文件目录及模板目录，在设置中指定
- 添加富文本编辑器配置及app注册
