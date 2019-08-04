import abc
from passlib.hash import sha256_crypt
from connector import ConnectorStrategy

import redis
import uuid
from datetime import datetime
import operator

class RedisConnector(ConnectorStrategy):
  def connect(self,app):
    self.r = redis.Redis()
    try:
        app.config['SECRET_KEY'] = 'redis_vuongnq4'
        conn = redis.StrictRedis(
                    host='localhost',
                    port=6379,
                    decode_responses=True,
                    db=1)
        conn.ping()
        self.r = conn
    except Exception as ex:
        print('Error')

  def valid_login(self,username,password):
    for key in self.r.scan_iter('users:*'):
        data = self.r.hgetall(key)
        if data['username']==username and data['password']==password:
            data['id'] = key
            return data

    return None

  def create_user(self,username,email,password):
    key='users:'+str(uuid.uuid1())
    user = {
        'username': username,
        'password': password,
        'email': email,
        'created_at': str(datetime.now()),
        'is_active': '0'
    }
    self.r.hmset(key,user)

  def check_exist(self,username):
    for key in self.r.scan_iter('users:*'):
        data = self.r.hgetall(key)
        if data['username'] == username:
            data['id'] = key
            return data
    return {}

  def set_status_user(self,userid,is_active):
    data = self.r.hgetall(userid)
    if is_active == True:
        data['is_active'] = '1'
    else:
        data['is_active'] = '0'
    self.r.hmset(userid,data)

  def fetch_all_users(self):
    users = {}
    for key in self.r.scan_iter('users:*'):
        data = self.r.hgetall(key)
        users[key]=(data['username'],data['is_active'])
    return users

  def fetch_all_group(self):
    room_lists = {}
    for key1 in self.r.scan_iter('conversation:*'):
        data1 = self.r.hgetall(key1)
        if data1['is_group']=='1':
            key2=data1['creator_id']
            data2=self.r.hgetall(key2)
            room_lists[key1]=(data1['title'],data2['username'])

    return room_lists

  def fetch_all_group_users(self):
    room_users={}

    for key1 in self.r.scan_iter('conversation:*'):
        data1 = self.r.hgetall(key1)
        if data1['is_group']=='1':
            room_users[key1]=[]
            for key2 in self.r.scan_iter('participants:*'):
                data2=self.r.hgetall(key2)
                if key1==data2['conversation_id'] and data1['creator_id']!=data2['user_id']:
                    data3=self.r.hgetall(data2['user_id'])
                    room_users[key1].append(data3['username'])      
    return room_users

  def have_private_chat(self,userid1,userid2):
    conversations1 = []
    conversations2 = []
    for key in self.r.scan_iter('participants:*'):
        data=self.r.hgetall(key)
        if self.r.hgetall(data['conversation_id'])['is_group']=='0':
            if data['user_id']==userid1:
                conversations1.append(data['conversation_id'])
            elif data['user_id']==userid2:
                conversations2.append(data['conversation_id'])

    data={}
    for ele1 in conversations1:
        for ele2 in conversations2:
            if ele1 == ele2:
                data['id'] = ele1
                return data
    return {}

  def create_private_chat(self,userid1,userid2):
    key1 = 'conversation:'+str(uuid.uuid1())
    value1 = {
        'title': '',
        'creator_id': userid1,
        'created_at': str(datetime.now()),
        'is_group': '0'
    }
    self.r.hmset(key1,value1)

    key2 = 'participants:'+str(uuid.uuid1())
    value2={
        'conversation_id': key1,
        'user_id': userid1,
        'created_at': str(datetime.now())
    }
    self.r.hmset(key2,value2)

    key3 = 'participants:'+str(uuid.uuid1())
    value3={
        'conversation_id': key1,
        'user_id': userid2,
        'created_at': str(datetime.now())
    }
    self.r.hmset(key3,value3)
    return key1

  def get_username(self,userid):
    return self.r.hgetall(userid)['username']

  def fetch_private_chats(self,conversation_id):
    list_chats = []

    for key in self.r.scan_iter('messages:*'):
        data=self.r.hgetall(key)
        if self.r.hgetall(conversation_id)['is_group']=='0' and data['conversation_id']==conversation_id:
            content = {
                        'username': self.r.hgetall(data['sender_id'])['username'],
                        'message': data['message'],
                        'created_at': data['created_at']
                    }
            list_chats.append(content)

    list_chats.sort(key = operator.itemgetter('created_at'), reverse=False)

    return list_chats

  def insert_message(self,conversation_id,sender_id,message):
    key1 = 'messages:'+str(uuid.uuid1())
    value1 = {
        'conversation_id': conversation_id,
        'sender_id': sender_id,
        'message': message,
        'created_at': str(datetime.now())
    }
    self.r.hmset(key1,value1)

    users=[]
    for key in self.r.scan_iter('participants:*'):
        data=self.r.hgetall(key)
        if data['conversation_id']==conversation_id and data['user_id']!=sender_id:
            key2 = 'message_status:'+str(uuid.uuid1())
            value2 = {
                'conversation_id': conversation_id,
                'message_id': key1,
                'receiver_id': data['user_id'],
                'is_seen': '0'
            }
            self.r.hmset(key2,value2)


  def create_room(self,title,user_id):
    key1 = 'conversation:'+str(uuid.uuid1())
    value1 = {
        'title': title,
        'creator_id': user_id,
        'created_at': str(datetime.now()),
        'is_group': '1'
    }
    self.r.hmset(key1,value1)

    key2='participants:'+str(uuid.uuid1())
    value2={
        'conversation_id': key1,
        'user_id': user_id,
        'created_at': str(datetime.now())
    }
    self.r.hmset(key2,value2)
    return key1

  def fetch_group_users(self,conversation_id):
    room_users={}

    for key in self.r.scan_iter('participants:*'):
        data=self.r.hgetall(key)
        if data['conversation_id']==conversation_id and self.r.hgetall(conversation_id)['is_group']=='1':
            room_users[data['user_id']]=(self.r.hgetall(data['user_id'])['username'])

    return room_users

  def check_user_in_room(self,conversation_id,user_id):
    user_in_room = {}

    for key in self.r.scan_iter('participants:*'):
        data=self.r.hgetall(key)
        if data['conversation_id']==conversation_id and self.r.hgetall(conversation_id)['is_group']=='1' and data['user_id']==user_id:
            user_in_room['title']=self.r.hgetall(conversation_id)['title']
            return user_in_room

    return user_in_room

  def fetch_room_chats(self,conversation_id):
    list_chats=[]

    for key in self.r.scan_iter('messages:*'):
        data=self.r.hgetall(key)
        if self.r.hgetall(conversation_id)['is_group']=='1' and data['conversation_id']==conversation_id:
            content = {
                        'username': self.r.hgetall(data['sender_id'])['username'],
                        'message': data['message'],
                        'created_at': data['created_at']
                    }
            list_chats.append(content)

    list_chats.sort(key = operator.itemgetter('created_at'), reverse=False)
    
    return list_chats

  def list_message_receiver(self,conversation_id,message_id):
    return None

  def list_final_message_receiver(self,conversation_id):
    list_message_id = []

    for key in self.r.scan_iter('messages:*'):
        data=self.r.hgetall(key)
        if data['conversation_id']==conversation_id:
            content={
                'id': key,
                'created_at': data['created_at']
            }
            list_message_id.append(content)

    list_message_id.sort(key = operator.itemgetter('created_at'), reverse=True)
    
    message_id = list_message_id[0]['id']

    receivers = []

    for key in self.r.scan_iter('message_status:*'):
        data=self.r.hgetall(key)
        if data['conversation_id']==conversation_id and data['message_id']==message_id and data['is_seen']=='1':
            receivers.append(self.r.hgetall(data['receiver_id'])['username'])
    return receivers
  
  def set_message_received(self,conversation_id,receiver_id):
    for key in self.r.scan_iter('message_status:*'):
        data=self.r.hgetall(key)
        if data['conversation_id']==conversation_id and data['receiver_id']==receiver_id and data['is_seen']=='0':
            data['is_seen']='1'
            self.r.hmset(key,data)

  def join_room(self,conversation_id,user_id):
    key = 'participants:'+str(uuid.uuid1)
    value = {
        'conversation_id': conversation_id,
        'user_id': user_id,
        'created_at': str(datetime.now())
    }
    self.r.hmset(key,value)

  def fetch_all_conversation(self,user_id):
    conversation_list=[]
    for key in self.r.scan_iter('participants:*'):
        data=self.r.hgetall(key)
        if data['user_id']==user_id:
            content={
                'conversation_id': data['conversation_id']
            }
            conversation_list.append(content)
    return conversation_list

  def fetch_conversation_chats(self,conversation_id):
    list_chats = []
    return list_chats

  def is_room(self,conversation_id):
    data=self.r.hgetall(conversation_id)

    if data['is_group']=='1':
       return 'Room ' + str(data['title']) + ': '
    else:
        users=[]
        for key in self.r.scan_iter('participants:*'):
            data=self.r.hgetall(key)
            if data['conversation_id']==conversation_id:
                users.append({'user_id': data['user_id']})
        return users