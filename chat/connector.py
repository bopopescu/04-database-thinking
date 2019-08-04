import abc

class ConnectorStrategy():
    __metaclass__=abc.ABCMeta

    @abc.abstractmethod
    def connect(self,app):
        """Reqired Method"""

    @abc.abstractmethod
    def valid_login(self,username,password):
        """Reqired Method"""

    @abc.abstractmethod
    def create_user(self,username,email,password):
        """Reqired Method"""

    @abc.abstractmethod
    def check_exist(self,username):
        """Reqired Method"""

    @abc.abstractmethod
    def set_status_user(self,userid,is_active):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_all_users(self):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_all_group(self):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_all_group_users(self):
        """Reqired Method"""

    @abc.abstractmethod
    def have_private_chat(self,userid1,userid2):
        """Reqired Method"""

    @abc.abstractmethod
    def create_private_chat(self,userid1,userid2):
        """Reqired Method"""

    @abc.abstractmethod
    def get_username(self,userid):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_private_chats(self,conversation_id):
        """Reqired Method"""

    @abc.abstractmethod
    def insert_message(self,conversation_id,sender_id,message):
        """Reqired Method"""

    @abc.abstractmethod
    def create_room(self,title,user_id):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_group_users(self,conversation_id):
        """Reqired Method"""

    @abc.abstractmethod
    def check_user_in_room(self,conversation_id,user_id):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_room_chats(self,conversation_id):
        """Reqired Method"""

    @abc.abstractmethod
    def list_message_receiver(self,conversation_id,message_id):
        """Reqired Method"""

    @abc.abstractmethod
    def list_final_message_receiver(self,conversation_id):
        """Reqired Method"""

    @abc.abstractmethod
    def set_message_received(self,conversation_id,receiver_id):
        """Reqired Method"""

    @abc.abstractmethod
    def join_room(self,conversation_id,user_id):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_all_conversation(self,user_id):
        """Reqired Method"""

    @abc.abstractmethod
    def fetch_conversation_chats(self,conversation_id):
        """Reqired Method"""

    @abc.abstractmethod
    def is_room(self,conversation_id):
        """Reqired Method"""

class Connector():
    def __init__(self, connectorStrategy):
        self.connectorStrategy = connectorStrategy
    
    def connect(self,app):
        self.connectorStrategy.connect(app)

    def valid_login(self, username, password):
        return self.connectorStrategy.valid_login(username,password)

    def create_user(self,username,email,password):
        return self.connectorStrategy.create_user(username,email,password)
        
    def check_exist(self,username):
        return self.connectorStrategy.check_exist(username)

    def set_status_user(self,userid,is_active):
        return self.connectorStrategy.set_status_user(userid,is_active)

    def fetch_all_users(self):
        return self.connectorStrategy.fetch_all_users()

    def fetch_all_group(self):
        return self.connectorStrategy.fetch_all_group()

    def fetch_all_group_users(self):
        return self.connectorStrategy.fetch_all_group_users()

    def have_private_chat(self,userid1,userid2):
        return self.connectorStrategy.have_private_chat(userid1,userid2)

    def create_private_chat(self,userid1,userid2):
        return self.connectorStrategy.create_private_chat(userid1,userid2)

    def get_username(self,userid):
        return self.connectorStrategy.get_username(userid)

    def fetch_private_chats(self,conversation_id):
        return self.connectorStrategy.fetch_private_chats(conversation_id)

    def insert_message(self,conversation_id,sender_id,message):
        return self.connectorStrategy.insert_message(conversation_id,sender_id,message)

    def create_room(self,title,user_id):
        return self.connectorStrategy.create_room(title,user_id)

    def fetch_group_users(self,conversation_id):
        return self.connectorStrategy.fetch_group_users(conversation_id)

    def check_user_in_room(self,conversation_id,user_id):
        return self.connectorStrategy.check_user_in_room(conversation_id,user_id)

    def fetch_room_chats(self,conversation_id):
        return self.connectorStrategy.fetch_room_chats(conversation_id)

    def list_message_receiver(self,conversation_id,message_id):
        return self.connectorStrategy.list_message_receiver(conversation_id,message_id)

    def list_final_message_receiver(self,conversation_id):
        return self.connectorStrategy.list_final_message_receiver(conversation_id)

    def set_message_received(self,conversation_id,receiver_id):
        return self.connectorStrategy.set_message_received(conversation_id,receiver_id)

    def join_room(self,conversation_id,user_id):
        return self.connectorStrategy.join_room(conversation_id,user_id)

    def fetch_all_conversation(self,user_id):
        return self.connectorStrategy.fetch_all_conversation(user_id)

    def fetch_conversation_chats(self,conversation_id):
        return self.connectorStrategy.fetch_conversation_chats(conversation_id)

    def is_room(self,conversation_id):
        return self.connectorStrategy.is_room(conversation_id)