from tortoise import fields, models


#当对模型进行更改时，可以运行以下命令来更新数据库：
#docker-compose exec backend aerich migrate
#docker-compose exec backend aerich upgrade
class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

# 单条对话记录
class Conversation(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.Users', related_name='conversations')
    user_message = fields.TextField()
    ai_message = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True)
    session = fields.ForeignKeyField(
        'models.ChatSession',
        related_name='conversations',
        null=True  # 允许单对话模式为空
    )

# 聊天对话容器
class ChatSession(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.Users', related_name='sessions')
    title = fields.CharField(max_length=200)  # 对话标题
    created_at = fields.DatetimeField(auto_now_add=True)
    conversations = fields.ReverseRelation['Conversation']  # 反向关系

def __str__(self):
    return f"{self.title}, {self.author_id} on {self.created_at}"