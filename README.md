# 基于FastApi、Vue、Ollama的智能对话系统

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
## Ollama
```
docker exec -it 你的Ollama容器id sh
ollama pull deepseek-r1:latest
```
自动创建的ollama_data文件夹与容器内.ollama文件夹对应，用于持久化模型，下次不用重复拉。模型在代码中默认为deepseek-r1:latest
## 前端 (localhost:8080)
（如果8080端口被占用会递增至8081端口）\
1、安装**Node.js**\
2、新开一个终端（根目录）输入命令
```
cd frontend
npm install
npm run serve
```
