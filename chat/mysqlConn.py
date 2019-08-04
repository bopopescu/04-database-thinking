import abc
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from passlib.hash import sha256_crypt
from connector import ConnectorStrategy

class MySqlConnector(ConnectorStrategy):
  def connect(self,app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '123456'
    app.config['MYSQL_DB'] = 'chat_app'
    app.config['SECRET_KEY'] = 'mysql_vuongnq4'

    self.mysql = MySQL(app)

  def valid_login(self,username,password):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cursor.execute('SELECT * FROM users WHERE username = %s',[username]) 
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s',(username,password)) 
    account = cursor.fetchone()
    cursor.close()
    if account:
      return account
    else:
      return None
    # if account and sha256_crypt.verify(password,account['password']):
    #   return account
    # else:
    #   return None

  def create_user(self,username,email,password):
    # Account doesnt exists and the form data is valid, now insert new account into accounts table
    #password = sha256_crypt.hash(password)
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO users (username, password, email, is_active) VALUES (%s, %s, %s, false)", (username, password, email))
    self.mysql.connection.commit()
    cursor.close()

  def check_exist(self,username):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", [username])
    account = cursor.fetchone()
    cursor.close()
    return account

  def set_status_user(self,userid,is_active):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if is_active == True:
        cursor.execute('UPDATE users SET is_active = true WHERE id=%s',[userid])
    else:
        cursor.execute('UPDATE users SET is_active = false WHERE id=%s',[userid])
    self.mysql.connection.commit()
    cursor.close()

  def fetch_all_users(self):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT username, id, is_active FROM users''')
    users = cursor.fetchall()
    cursor.close()
    return dict((ele['id'], (ele['username'],ele['is_active'])) for ele in users)

  def fetch_all_group(self):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT c.id, c.title, u.username FROM conversation as c JOIN users as u ON u.id = c.creator_id WHERE c.is_group=true''')
    room_lists = cursor.fetchall()
    cursor.close()
    return dict((ele['id'], (ele['title'], ele['username'])) for ele in room_lists)

  def fetch_all_group_users(self):
      room_lists = self.fetch_all_group()

      cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('''SELECT c.id, u.username FROM conversation as c JOIN users as u JOIN participants as p ON p.conversation_id = c.id AND p.user_id = u.id AND u.id != c.creator_id WHERE c.is_group=true''')
      temp_room_users = cursor.fetchall()

      room_users={}
      list_users=[]
      for key in room_lists.keys():
          list_users=[]
          for ele in temp_room_users:
              if(ele['id'] == key):
                  list_users.append(ele['username'])
          room_users[key] = list_users
      cursor.close()
      return room_users

  def have_private_chat(self,userid1,userid2):
      cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT c1.id FROM conversation as c1 JOIN participants as p1 ON c1.id=p1.conversation_id WHERE c1.is_group=false AND p1.user_id=%s AND c1.id IN (SELECT c2.id FROM conversation as c2 JOIN participants as p2 ON c2.id=p2.conversation_id WHERE c2.is_group=false AND p2.user_id=%s)',(userid1,userid2))
      have_chat = cursor.fetchone()
      cursor.close()
      return have_chat

  def create_private_chat(self,userid1,userid2):
      cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('INSERT INTO conversation (creator_id,is_group) VALUES (%s,false)',[userid1])

      self.mysql.connection.commit()
      conversation_id = cursor.lastrowid

      cursor.execute('INSERT INTO participants (conversation_id,user_id) VALUES (%s,%s)',(conversation_id,userid1))
      self.mysql.connection.commit()

      cursor.execute('INSERT INTO participants (conversation_id,user_id) VALUES (%s,%s)',(conversation_id,userid2))
      self.mysql.connection.commit()

      cursor.close()

      return conversation_id

  def get_username(self,userid):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username FROM users WHERE id=%s',[userid])

    username = cursor.fetchone()['username']
    cursor.close()
    return username

  def fetch_private_chats(self,conversation_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.username, m.message FROM messages as m JOIN conversation as c JOIN users as u ON c.id=m.conversation_id AND u.id=m.sender_id WHERE c.id=%s AND c.is_group=false ORDER BY m.created_at ASC',[conversation_id])

    list_chats=cursor.fetchall()

    cursor.close()

    return list_chats

  def insert_message(self,conversation_id,sender_id,message):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO messages (conversation_id,sender_id,message) VALUES (%s, %s,%s)',(conversation_id,sender_id,message))
    self.mysql.connection.commit()
    message_id = cursor.lastrowid

    cursor.execute('SELECT user_id FROM participants WHERE conversation_id=%s',[conversation_id])

    users = cursor.fetchall()

    for ele in users:
      if ele['user_id'] != sender_id:
        cursor.execute('INSERT INTO message_status (conversation_id,message_id,receiver_id) VALUES (%s,%s,%s)',(conversation_id,message_id,ele['user_id']))
        self.mysql.connection.commit()

    cursor.close()

  def create_room(self,title,user_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO conversation (title,creator_id) VALUES (%s,%s)', (title,user_id))

    self.mysql.connection.commit()
    conversation_id=cursor.lastrowid

    cursor.execute('INSERT INTO participants (conversation_id,user_id) VALUES (%s,%s)',(conversation_id,user_id))
    self.mysql.connection.commit()

    cursor.close()
    return conversation_id

  def fetch_group_users(self,conversation_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.id, u.username FROM conversation as c JOIN users as u JOIN participants as p ON p.conversation_id = c.id AND p.user_id = u.id WHERE c.id = %s AND c.is_group=true', [conversation_id])

    room_users=dict((ele['id'],ele['username']) for ele in cursor.fetchall())
    cursor.close()

    return room_users

  def check_user_in_room(self,conversation_id,user_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT title FROM participants as p JOIN conversation as c ON c.id=p.conversation_id WHERE c.id = %s AND p.user_id = %s AND c.is_group=true',(conversation_id, user_id))
    user_in_room = cursor.fetchone()
    cursor.close()
    return user_in_room

  def fetch_room_chats(self,conversation_id):

    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.username, m.message, m.id FROM conversation as c JOIN messages as m JOIN users as u ON m.sender_id=u.id AND m.conversation_id=c.id WHERE m.conversation_id=%s AND c.is_group=true ORDER BY m.created_at ASC',[conversation_id])

    list_chats = cursor.fetchall()
    cursor.close()
    return list_chats

  def list_message_receiver(self,conversation_id,message_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.username FROM message_status as ms JOIN users as u ON ms.receiver_id=u.id WHERE ms.conversation_id=%s AND ms.message_id=%s AND ms.is_seen = true',(conversation_id,message_id))
    receivers = cursor.fetchall()
    cursor.close()
    return receivers

  def list_final_message_receiver(self,conversation_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM messages WHERE conversation_id=%s ORDER BY created_at DESC LIMIT 1',[conversation_id])

    message_id = cursor.fetchone()['id']

    cursor.execute('SELECT u.username FROM message_status as ms JOIN users as u ON ms.receiver_id=u.id WHERE ms.conversation_id=%s AND ms.message_id=%s AND ms.is_seen = true',(conversation_id,message_id))
    receivers = cursor.fetchall()
    cursor.close()
    return receivers
  
  def set_message_received(self,conversation_id,receiver_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE message_status SET is_seen = true WHERE conversation_id=%s AND receiver_id=%s AND is_seen=false',(conversation_id,receiver_id))
    self.mysql.connection.commit()
    cursor.close()


  def join_room(self,conversation_id,user_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO participants (conversation_id,user_id) VALUES (%s, %s)',(conversation_id,user_id))
    self.mysql.connection.commit()
    cursor.close()

  def fetch_all_conversation(self,user_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT conversation_id FROM participants WHERE user_id=%s',[user_id])
    conversation_list = list(cursor.fetchall())
    cursor.close()
    return conversation_list

  def fetch_conversation_chats(self,conversation_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.username, m.message FROM messages as m JOIN conversation as c JOIN users as u ON c.id=m.conversation_id AND u.id=m.sender_id WHERE c.id=%s ORDER BY m.created_at ASC',[conversation_id])

    list_chats=cursor.fetchall()

    cursor.close()

    return list_chats

  def is_room(self,conversation_id):
    cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT is_group, title FROM conversation WHERE id=%s',[conversation_id])
    data = cursor.fetchone()
    cursor.close()
    flag = bool(data['is_group'])
    if flag:
      return 'Room ' + str(data['title']) + ': '
    else:
      cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT user_id FROM participants WHERE conversation_id=%s',[conversation_id])
      data = cursor.fetchall()
      cursor.close()
      return data