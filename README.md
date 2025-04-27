# 基于FastAPI、Vue、Ollama的AI对话系统

## 没做的地方！
1、没有做AI上下文和流式输出\
2、前端样式没有做到预期\
3、会话id没有做删除后回退，这样后面新建的会话数字不连续，而且所有用户没有自己独立的id序列\
4、没有做将会话内容总结为会话标题\
5、新进入如果不选择会话就聊天不会在左边新建一个会话，并且在这个时候点击左边的不会有反应\
6、前端注册功能有问题\
7、登录如果输入错误的用户名或密码，前端跳转有点小问题
## 后端 (localhost:5000)
1、安装**docker**（最好用命令行安装，否则会默认安装到C盘）\
2、启动docker\
3、在终端（根目录）输入命令
```
docker pull python:3.11-buster

docker-compose up -d --build # 后台启动后端、Ollama和数据库服务，如果要在前台启动可以去掉-d参数

docker-compose exec backend aerich init -t src.core.database.config.TORTOISE_ORM # 初始化aerich
docker-compose exec backend aerich init-db # 初始化数据库 生成migrations/models里的文件 如果文件已存在的时候重复执行会报错 删除models文件夹即可
```
后端启动完成\
\
*另外，如果修改了数据库模型，需要在根目录输入命令以更新（或者删除migrations里的models并重新执行上一段命令）
```
docker-compose exec backend aerich migrate
docker-compose exec backend aerich upgrade
```
*可使用localhost:5000/docs测试后端接口
## Ollama
```
docker exec -it 你的Ollama容器id sh
ollama pull deepseek-r1:latest
```
自动创建的ollama_data文件夹与容器内.ollama文件夹对应，用于持久化模型，下次不用重复拉。模型在代码中默认为deepseek-r1:latest\
如果要换模型，前后端都有要改的地方
## 前端 (localhost:8080)
（如果8080端口被占用会递增至8081端口）\
1、安装**Node.js**\
2、新开一个终端（根目录）输入命令
```
cd frontend
npm install
npm run serve
```
## 项目结构
```
llm-chat-page/
├── backend/                         # 后端服务
│   ├── Dockerfile                   # 后端Docker配置
│   ├── migrations/                  # 数据库迁移文件
│   │   └── models/                  # 数据库模型
│   ├── pyproject.toml               # Aerich配置
│   ├── requirements.txt             # Python依赖
│   └── src/
│       ├── core/
│       │   ├── auth/                # 认证相关
│       │   │   ├── jwthandler.py    # JWT处理
│       │   │   └── users.py         # 用户认证
│       │   ├── crud/                # 数据库操作
│       │   │   └── users.py         # 用户CRUD
│       │   ├── database/            # 数据库配置
│       │   │   ├── config.py        # ORM配置
│       │   │   ├── models.py        # 数据库模型定义
│       │   │   └── register.py      # ORM注册
│       │   ├── schemas/             # Pydantic模型
│       │   │   ├── token.py         # Token模型
│       │   │   └── users.py         # 用户模型
│       │   └── routes/              # API路由
│       │       ├── ollama_chat.py   # AI聊天路由
│       │       └── users.py         # 用户路由
│       └── main.py                  # FastAPI入口
│
├── frontend/                        # 前端Vue项目
│   ├── public/                      # 静态资源
│   │   ├── index.html               # 主HTML
│   │   └── *.svg                    # 图标资源
│   ├── src/
│   │   ├── components/              # Vue组件
│   │   │   ├── NavBar.vue           # 导航栏
│   │   │   └── SideBar.vue          # 侧边栏
│   │   ├── router                   # 路由管理
│   │   │   └── index.js
│   │   ├── store/                   # Vuex状态管理
│   │   │   ├── index.js             # 状态模块管理
│   │   │   └── modules/
│   │   │       └── users.js         # 用户状态
│   │   ├── views/                   # 页面视图
│   │   │   ├── ChatView.vue         # 聊天主界面
│   │   │   ├── LoginView.vue        # 登录页
│   │   │   └── RegisterView.vue     # 注册页
│   │   ├── App.vue                  # 根组件
│   │   └── main.js                  # 入口文件
│   ├── package.json                 # 前端依赖
│   ├── vue.config.js                # Vue配置
│   └── babel.config.js              # Babel配置
├── .gitattributes                   # Git换行符规则
├── docker-compose.yml               # 容器编排
├── README.md                        # 项目说明
└── .gitignore                       # Git忽略规则
```
## 效果图
![image](https://github.com/user-attachments/assets/e3fc68f1-07fd-4b7d-ac6c-9c0d3c6625f6)![image](https://github.com/user-attachments/assets/d8463091-5d6b-4ca3-9a27-4f27d7c0bd76)

