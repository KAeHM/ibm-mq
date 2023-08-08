import pymqi
import time
import json
import os

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

    def warning(self, message):
        print(self.WARNING + message + self.ENDC)
    

class ClientMQ:

    # Queue Manager Configuration

    queue_manager = None
    host = None
    port = None
    conn_info = f'{host}({port})' 

    qmgr_connection = None

    # User Configuration

    user = None
    password = None

    # Channel Configuration

    channel = None
     
    # Queue Configuration 

    queue_name = None

    queue_connection = None


    def start_connection(self):
        try:
            if self.qmgr_connection == None:
                self.qmgr_connection = pymqi.connect(self.queue_manager, self.channel, self.conn_info, self.user, self.password)
                message="SUCCESSFULLY CONECTED TO QUEUE MANAGER: " + str(self.qmgr_connection)
                beautify().success(message=message)
                return self.qmgr_connection
            else:
                beautify().fail('QUEUE MANAGER ALREADY CONNECTED')
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
        
    def get_envs(self):
        self.queue_manager = os.environ.get('IBM_CLIENT_QM') if os.environ.get('IBM_CLIENT_QM') != None else None
        self.host = os.environ.get('IBM_CLIENT_HOST') if os.environ.get('IBM_CLIENT_HOST') != None else None
        self.port =  os.environ.get('IBM_CLIENT_PORT') if os.environ.get('IBM_CLIENT_PORT') != None else None
        self.user =  os.environ.get('IBM_CLIENT_USER') if os.environ.get('IBM_CLIENT_USER') != None else None
        self.password =  os.environ.get('IBM_CLIENT_PASSWROD') if os.environ.get('IBM_CLIENT_PASSWROD') != None else None 
        self.channel =  os.environ.get('IBM_CLIENT_CHANNEL') if os.environ.get('IBM_CLIENT_CHANNEL') != None else None 
        self.queue_name =  os.environ.get('IBM_CLIENT_QUEUE') if os.environ.get('IBM_CLIENT_QUEUE') != None else None

    def close_queue(self):
        try:
            self.queue_connection.close()
            self.queue_connection = None
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
    
    def put_message(self, message, quantity):
        message_descriptor = pymqi.MD()

        for __ in range(0, quantity):
            try:
                self.queue_connection.put(message, message_descriptor)

                message_obj = {
                        "message": message,
                        "msg_id": message_descriptor.MsgId.hex(),
                        "msg_user": message_descriptor.UserIdentifier.decode('utf-8')
                }

                json_obj = json.dumps(message_obj)
                beautify().display(json_obj)

                message_descriptor.MsgId = pymqi.CMQC.MQMI_NONE
                
            except Exception as error:
                beautify().fail('ERROR: ' + str(error))
                return error
        beautify().success("MESSAGES SENDED!")
        time.sleep(3)

    def get_message(self, quantity):
        message_descriptor = pymqi.MD()
        for __ in range(0, quantity):
            try:
                message = self.queue_connection.get(None, message_descriptor)
                beautify().display(message=message.decode('utf-8'))
            except Exception as error:
                beautify().fail('ERROR: ' + str(error))
                return error
        time.sleep(3)
    
    def wait_for_message(self):
        message_descriptor = pymqi.MD()

        get_message_options = pymqi.GMO()
        get_message_options.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        get_message_options.WaitInterval = 5000 

        keep_running = True
        try:
            while keep_running:
                try:
                    message = self.queue_connection.get(None, message_descriptor, get_message_options)
                    message_obj = {
                        "message": message.decode('utf-8'),
                        "msg_id": message_descriptor.MsgId.hex(),
                        "msg_user": message_descriptor.UserIdentifier.decode('utf-8')
                    }
                    json_obj = json.dumps(message_obj)
                    beautify().display(message=json_obj)

                    message_descriptor.MsgId = pymqi.CMQC.MQMI_NONE
                    message_descriptor.CorrelId = pymqi.CMQC.MQCI_NONE
                    message_descriptor.GroupId = pymqi.CMQC.MQGI_NONE
                except pymqi.MQMIError as error:
                    if error.comp == pymqi.CMQC.MQCC_FAILED and error.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                        pass
                    else:
                        raise
        except KeyboardInterrupt:
            keep_running = False
            pass
    
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
    
    def qmgr_desconnect(self):
        self.clientmq.finish_connection()
        time.sleep(2)

    def send_message(self):
        self.clientmq.open_queue()
        time.sleep(2)

        if self.clientmq.queue_connection != None:
            message = input('Message content: ')
            quantity = int(input('Quantity of same message: '))
        
            self.clientmq.put_message(message=message, quantity=quantity)

            self.clientmq.close_queue()
            time.sleep(2)

    
    def retrieve_message(self):
        self.clientmq.open_queue()
        time.sleep(2)

        if self.clientmq.queue_connection != None:
            quantity = int(input('Quantity of messages: '))
        
            self.clientmq.get_message(quantity=quantity)

            self.clientmq.close_queue()
            time.sleep(2)
    
    def listening_message(self):
        self.clientmq.open_queue()
        time.sleep(2)

        if self.clientmq.queue_connection != None:
            self.clientmq.wait_for_message()

            self.clientmq.close_queue()
            time.sleep(2)

    def start_client(self):
        running = True
        self.clientmq.get_envs()
        while running:
            try:
                self.header()
                beautify().format_output(' [1] Settings\n [2] Messages \n [3] Connection \n [4] Exit')
                choose_action = int(input('Choose a action: '))
                if choose_action == 1:
                    obj = {1: self.configure_queue_manager, 2: self.configure_user, 3: self.configure_channel, 4: self.configure_queue, 5: print}
                    beautify().format_output(' [1] Configure Queue Manager\n [2] Configure User\n [3] Configure Channel\n [4] Configure Queue, \n [5] Back')
                    choose_methods = int(input('Choose a action: '))
                    if choose_methods > len(obj) or choose_methods < 1: 
                        beautify().fail('INVALID RANGE')
                        time.sleep(2)
                    else:
                        obj[choose_methods]()

                elif choose_action == 2:
                    obj = {1: self.send_message, 2: self.retrieve_message, 3: self.listening_message, 4: print}
                    beautify().format_output(' [1] Send Message\n [2] Retrieve Message\n [3] Litening Message\n [4] Back')
                    choose_methods = int(input('Choose a action: '))
                    if choose_methods > len(obj) or choose_methods < 1: 
                        beautify().fail('INVALID RANGE')
                        time.sleep(2)
                    else:
                        obj[choose_methods]()
                    
                elif choose_action == 3:
                    obj = {1: self.qmgr_connection, 2: self.qmgr_desconnect, 3: print}
                    beautify().format_output(' [1] Start Queue Manager Connection\n [2] Stop Queue Manager Connection\n [3] Back')
                    choose_methods = int(input('Choose a action: '))
                    if choose_methods > len(obj) or choose_methods < 1: 
                        beautify().fail('INVALID RANGE')
                        time.sleep(2)
                    else:
                        obj[choose_methods]()
                
                elif choose_action == 4:
                    beautify().success('PROGRAM EXITED WITH STATUS 0')
                    exit(0)

            except ValueError as error:
                if 'main.py' in str(error):
                    beautify().success('PROGRAM EXITED WITH STATUS 0')
                    exit(0)
                else:
                    beautify().fail('INVALID INPUT')
                    time.sleep(2)
            except KeyboardInterrupt:
                print('\n')
                beautify().warning('Tem certeza que deseja sair ? [S/N] ')
                response = input('').lower()
                if response == 's':
                    beautify().success('PROGRAM EXITED WITH STATUS 0')
                    exit(0)
                else:
                    pass

ClientInterface().start_client()

