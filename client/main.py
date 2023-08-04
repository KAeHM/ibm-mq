import pymqi
import time

class beautify:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def format_output(self, content):
        print('=' * 50)
        print(' ')
        print(content)
        print(' ')
        print('=' * 50)

    def success(self, message):
        print(self.OKGREEN + message + self.ENDC)

    def display(self, message):
        print(self.OKCYAN + message + self.ENDC)

    def fail(self, message):
        print(self.FAIL + message + self.ENDC)
    

class ClientMQ:

    # Queue Manager Configuration

    queue_manager = 'CSD' # CSD
    host = 'mq1' # mq1
    port = '1414' # 1414
    conn_info = f'{host}({port})' # mq1(1414)

    qmgr_connection = None

    # User Configuration

    user = 'kaehm' # kaehm
    password = '123456' # 123456

    # Channel Configuration

    channel = "PYTHON.APLICATION" # PYTHON.APLICATION
     
    # Queue Configuration 

    queue_name = "TEST.QUEUE"

    queue_connection = None


    def start_connection(self):
        try:
            self.qmgr_connection = pymqi.connect(self.queue_manager, self.channel, self.conn_info, self.user, self.password)
            message="SUCCESSFULLY CONECTED TO QUEUE MANAGER: " + str(self.qmgr_connection)
            beautify().success(message=message)
            return self.qmgr_connection
        except Exception as error:
            message = 'ERROR: ' + str(error)
            beautify().fail(message=message)
            return error

    def finish_connection(self):
        try:
            self.qmgr_connection.disconnect()
            self.qmgr_connection = None
            beautify().success("SUCCESSFULLY DISCONECTED FROM QUEUE MANAGER")
            return self.qmgr_connection
        except Exception as error:
            beautify().fail('ERROR: ' + str(error))
            return error
    
    def open_queue(self):
        try:
            if self.qmgr_connection == None:
                raise Exception("QUEUE MANAGER IS NOT CONNECTED!")

            self.queue_connection = pymqi.Queue(self.qmgr_connection, self.queue_name)
            beautify().success("SUCCESSFULLY CONECTED TO QUEUE: " + str(self.queue_connection))
            return self.queue_connection
        except Exception as error:
            beautify().fail('ERROR: ' + str(error))
            return error

    def close_queue(self):
        try:
            self.queue_connection.close()
            beautify().success("SUCCESSFULLY DISCONECTED FROM QUEUE")
            return self.queue_connection
        except Exception as error:
            beautify().fail('ERROR: ' + str(error))
            return error
    
    def display_config(self):
        return {
            'qm_config': {'queue_manager': self.queue_manager, 'host': self.host, 'port': self.port, 'conn_info': self.conn_info, 'qmgr_connection': self.qmgr_connection}, 
            'user_config': {'user': self.user, 'password': '*****'+ self.password[-2:-1] if self.password != None else None},
            'channel_config': {'channel': self.channel},
            'queue_config': {'queue_name': self.queue_name, 'queue_connection': self.queue_connection} 
            }
    
    def reset_config(self):
        self.queue_manager = None
        self.host = None
        self.port = None
        self.conn_info = f'{self.host}({self.port})'
        self.qmgr_connection = None
        self.user = None
        self.password = None
        self.channel = None 
        self.queue_name = None
        self.queue_connection = None
    
    def put_message(self, message, quantity):
        for __ in range(0, quantity):
            try:
                self.queue_connection.put(message)
            except Exception as error:
                beautify().fail('ERROR: ' + str(error))
                return error
        beautify().success("MESSAGES SENDED!")
        time.sleep(3)

    def get_message(self, quantity):
        for __ in range(0, quantity):
            try:
                message = self.queue_connection.get()
                beautify().display(message=message.decode('utf-8'))
            except Exception as error:
                beautify().fail('ERROR: ' + str(error))
                return error
        time.sleep(3)
    


class ClientInterface:
    clientmq = ClientMQ()
    
    def header(self):
        configs_obj = self.clientmq.display_config()
        print('=' * 50)
        print(' ')
        print('--- Queue Manager ---')
        print('NAME: ' + str(configs_obj['qm_config']['queue_manager']))
        print('HOST: ' + str(configs_obj['qm_config']['host']))
        print('PORT: ' + str(configs_obj['qm_config']['port']))
        verificate_conn = "OK" if configs_obj['qm_config']['qmgr_connection'] != None else "PENDING"
        print('CONNECTION STATUS: ' + verificate_conn)
        print(' ')
        print('--- User ---')
        print('NAME: ' + str(configs_obj['user_config']['user']))
        print('PASSWORD: ' + str(configs_obj['user_config']['password']))
        print(' ')
        print('--- Channel ---')
        print('NAME: ' + str(configs_obj['channel_config']['channel']))
        print(' ') 
        print('--- Queue ---')
        print('NAME: ' + str(configs_obj['queue_config']['queue_name']))
        verificate_conn = "OPEN" if configs_obj['queue_config']['queue_connection'] != None else "PENDING"
        print('CONNECTION STATUS: ' + verificate_conn)
        print(' ')

    def configure_queue_manager(self):
        print('=' * 50)
        self.clientmq.queue_manager = input('Queue Manager Name: ')
        self.clientmq.host = input('Host Address: ')
        self.clientmq.port = input('Port: ')
        self.clientmq.conn_info = f'{self.clientmq.host}({self.clientmq.port})'
        beautify().success('SUCCESSFULLY APPLIED')
        time.sleep(2)
    
    def configure_user(self):
        print('=' * 50)
        self.clientmq.user = input('User Name: ')
        self.clientmq.password = input('Password: ')
        beautify().success('SUCCESSFULLY APPLIED')
        time.sleep(2)

    def configure_channel(self):
        print('=' * 50)
        self.clientmq.channel = input('Channel Name: ')
        beautify().success('SUCCESSFULLY APPLIED')
        time.sleep(2)
        
    def configure_queue(self):
        print('=' * 50)
        self.clientmq.queue_name = input('Queue Name: ')
        beautify().success('SUCCESSFULLY APPLIED')
        time.sleep(2)

    def qmgr_connection(self):
        self.clientmq.start_connection()
        time.sleep(2)

    def send_message(self):
        self.clientmq.open_queue()
        time.sleep(2)

        if self.clientmq.queue_connection != None:
            message = input('Message content: ')
            quantity = int(input('Quantity of same message: '))
        
            self.clientmq.put_message(message=message, quantity=quantity)

            self.clientmq.close_queue()
            self.clientmq.queue_connection = None
            time.sleep(2)
    
    def retrieve_message(self):
        self.clientmq.open_queue()
        time.sleep(2)

        if self.clientmq.queue_connection != None:
            quantity = int(input('Quantity of messages: '))
        
            self.clientmq.get_message(quantity=quantity)

            self.clientmq.close_queue()
            self.clientmq.queue_connection = None
            time.sleep(2)

    def start_client(self):
        running = True
        while running:
            self.header()
            beautify().format_output(' [1] Settings\n [2] Requests \n [3] Connection \n [4] Exit')
            choose_action = int(input('Choose a action: '))
            if choose_action == 1:
                obj = {1: self.configure_queue_manager, 2: self.configure_user, 3: self.configure_channel, 4: self.configure_queue}
                beautify().format_output(' [1] Configure Queue Manager\n [2] Configure User\n [3] Configure Channel\n [4] Configure Queue')
                choose_methods = int(input('Choose a action: '))
                if choose_methods > len(obj) or choose_methods < 1: 
                    beautify().format_output('INVALID RANGE')
                    time.sleep(2)
                else:
                    obj[choose_methods]()

            elif choose_action == 2:
                obj = {1: self.qmgr_connection, 2: self.send_message, 3: self.retrieve_message}
                beautify().format_output(' [1] Queue Manager Connection\n [2] Send Message\n [3] Retrieve Message\n [4] Back')
                choose_methods = int(input('Choose a action: '))
                if choose_methods > len(obj) or choose_methods < 1: 
                    beautify().format_output('INVALID RANGE')
                    time.sleep(2)
                else:
                    obj[choose_methods]()

ClientInterface().start_client()

