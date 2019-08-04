from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from passlib.hash import sha256_crypt
from flask_socketio import SocketIO, Namespace, emit, disconnect, join_room, rooms, leave_room, close_room

from connector import Connector
from mysqlConn import MySqlConnector
from redisConn import RedisConnector

async_mode = None

app = Flask(__name__)

# redisConnector = RedisConnector()
# connector = Connector(redisConnector)
# connector.connect(app)


mySqlConnector = MySqlConnector()
connector = Connector(mySqlConnector)
connector.connect(app)

#app.secret_key = 'vuongnq4'
#SocketIO
socketio = SocketIO(app, async_mode=async_mode)

thread = None

def background_thread():
    count = 0
    while True:
        socketio.sleep(10)
        count += 1

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        account = connector.valid_login(username,password)
        if account is None:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        else:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('main_chat',username=username))
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    #sha256_crypt.encrypt(password)
    #sha256_crypt.verify(password_candidate, password)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # If account exists show error and validation checks
        if connector.check_exist(username):
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            connector.create_user(username,email,password)
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/<string:username>')
def main_chat(username):
    if 'loggedin' in session and username == session['username']:
        return render_template('chat.html', async_mode=socketio.async_mode)
    return redirect(url_for('login'))

class WebChat(Namespace):
    def on_connect(self):
        global thread
        #clients.append(session['id'])
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

    def on_register(self, message):
        connector.set_status_user(session['id'],True)

        users = connector.fetch_all_users()
        room_lists = connector.fetch_all_group()
        room_users = connector.fetch_all_group_users()

        conversation_list = connector.fetch_all_conversation(session['id'])
        for ele in conversation_list:
            join_room(ele['conversation_id'])

        # Broadcast that there is user is connected
        emit('user_response', {
                'type': 'connect',
                'message': '{0} is connected to the server'.format(session['username']),
                'data': {
                    'users': users,
                    'rooms': room_lists,
                    'room_users': room_users
                },
            }, broadcast=True)
        

    def on_private_message(self, message):
        if session['id'] != message['user']:
            have_chat = connector.have_private_chat(session['id'],message['user'])
            if not have_chat:

                conversation_id = connector.create_private_chat(session['id'],message['user'])
            else:
                conversation_id=have_chat['id']

            join_room(conversation_id)

            username = connector.get_username(message['user'])

            emit('message_response', {
                        'type': 'open_room',
                        'data': {
                            'room': conversation_id,
                            'room_name': 'Private: '+username
                        },
                    })

            list_chats = connector.fetch_private_chats(conversation_id)


            for ele in list_chats:
                    emit('message_response', {
                        'type': 'room_message',
                        'data': {
                            'text': ele['message'],
                            'room': conversation_id,
                            'from': ele['username'],
                        }
                    })

    def on_private_send(self, message):
        print('helloworld')
        

    def on_room_send(self, message):
        temp_room_name = message['user'].split('_')

        room_name = '_'.join(temp_room_name[1:len(temp_room_name)])
        
        if room_name.isdigit() == True:
            room_name=int(room_name)
        
        connector.insert_message(room_name,session['id'],message['text'])

        emit('message_response', {
                'type': 'room_message',
                'data': {
                    'text': message['text'],
                    'room': room_name,
                    'from': session['username'],
                }
            }, room=room_name)

        name = connector.is_room(room_name)

        feed='x'
        if type(name) is str:
            feed = name
        else:
            for ele in name:
                if ele['user_id'] != session['id']:
                    name = connector.get_username(ele['user_id'])
                    feed = 'User ' + session['username'] + ': '
                    break

        emit('feed_response', {
                    'type': 'feed',
                    'message': feed + ' sent-> '+message['text'],
                    'data': False,
                },room=room_name)

    def on_close_chat(self, message):
        print('NOT')

    def on_create_room(self, message):

        # If the room is not exist, append new room to rooms object, also set the admin and initial user
        if message['room'] is None:
            emit('feed_response', {
                    'type': 'feed',
                    'message': 'Room is exist, please use another room',
                    'data': False,
                })
        else:
            conversation_id = connector.create_room(message['room'],session['id'])

            room_lists = connector.fetch_all_group()
            room_users = connector.fetch_all_group_users()

            join_room(conversation_id)

            emit('feed_response', {
                    'type': 'rooms',
                    'message': '{0} created room {1}'.format(session['username'], message['room']),
                    'data': {
                        'rooms': room_lists,
                        'room_users': room_users
                    }
                }, broadcast=True)

            emit('message_response', {
                    'type': 'open_room',
                    'data': {
                        'room': conversation_id,
                        'room_name': message['room']
                    },
                })


    def on_get_room_users(self, message):
        room_users = connector.fetch_group_users(message['room'])

        if room_users:
            emit('feed_response', {
                    'type': 'room_users',
                    'message': '',
                    'data': room_users,
                    #'rooms': room_lists,
                })
            user_in_room = connector.check_user_in_room(message['room'],session['id'])

            if user_in_room:

                join_room(message['room'])

                emit('message_response', {
                        'type': 'open_room',
                        'data': {
                            'room': message['room'],
                            'room_name': user_in_room['title']
                        },
                    })

                list_chats = connector.fetch_room_chats(message['room'])

                for ele in list_chats:
                    emit('message_response', {
                        'type': 'room_message',
                        'data': {
                            'text': ele['message'],
                            'room': message['room'],
                            'from': ele['username'],
                        }
                    })

                

    def on_join_room(self, message):
        join_room(message['room'])

        connector.join_room(message['room'],session['id'])

        emit('feed_response', {
                'type': 'new_joined_users',
                'message': '{0} joined room id {1}'.format(session['username'], message['room']),
                #'data': list_users,
                'room': message['room'],
                'user_action': session['username'],
                'welcome_message': '{0} join the room'.format(session['username']),
            }, room=message['room'])
                

        room_lists = connector.fetch_all_group()

        room_users = connector.fetch_all_group_users()

        # Append to news feed that there is user joining the room
        emit('feed_response', {
            'type': 'rooms',
            'message': '',
            'data': {
                'rooms': room_lists,
                'room_users': room_users
            }
        }, broadcast=True)

        ###---
        # tell the frontend that this is the message for joining the room
        # open chat with id rooms_roomName
        emit('message_response', {
            'type': 'open_room',
            'data': {
                'room': message['room'],
            },
        })

        list_chats = connector.fetch_room_chats(message['room'])

        for ele in list_chats:
            emit('message_response', {
                'type': 'room_message',
                'data': {
                    'text': ele['message'],
                    'room': message['room'],
                    'from': ele['username'],
                }
            })

    def on_room_change(self,message):  

        if message['room'] is None:
            return
        if str(message['room']).isdigit() == True:
            message['room']=int(message['room'])

        connector.set_message_received(message['room'],session['id'])
        receivers = connector.list_final_message_receiver(message['room'])

        emit('message_response', {
            'type': 'room_feed',
            'data': {
                'room': message['room'],
                'text': 'Seen by: ' + str(receivers)
            },
        },room=message['room'])

    def on_close_room(self, message):
        print('NOT')

    def on_disconnect(self):
        connector.set_status_user(session['id'], False)

        users = connector.fetch_all_users()

        room_lists = connector.fetch_all_group()

        room_users = connector.fetch_all_group_users()

        # append to news feed
        emit('user_response', {
            'type': 'connect',
            'message': '{0} is disconnected from the server'.format(session['username']),
            'data': {
                'users': users,
                'rooms': room_lists,
                'room_users': room_users
            },
        }, broadcast=True)

        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)

    def on_my_ping(self):
        emit('my_pong')

socketio.on_namespace(WebChat('/chat'))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)