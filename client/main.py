import pymqi

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
        self.qmgr_connection = pymqi.connect(self.queue_manager, self.channel, self.conn_info, self.user, self.password)

    def finish_connection(self):
        self.qmgr_connection.disconnect()
    
    def open_queue(self):
        self.queue_connection = pymqi.Queue(self.qmgr_connection, self.queue_name)

    def close_queue(self):
        self.queue_connection.close()
    
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
            self.queue_connection.put(message)


class ClientInterface:
    clientmq = ClientMQ()

    def format_output(self, content):
        print('=' * 50)
        print(' ')
        print(content)
        print(' ')
        print('=' * 50)
    
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
        print('=' * 50)

    def configure_queue_manager(self):
        self.clientmq.queue_manager = input('Queue Manager Name: ')
        self.clientmq.host = input('Host Address: ')
        self.clientmq.port = input('Port: ')
        print('SUCCESSFULLY APPLIED')


    def start_client(self):
        running = True
        while running:
            self.header()
            print(' [1] Settings\n [2] Exit')
            choose_action = int(input('Choose a action: '))
            if choose_action == 1:
                obj = {1: self.configure_queue_manager}
                print(' [1] Configure Queue Manager\n [2] Configure User\n [3] Configure Channel\n [4] Configure Queue')
                choose_methods = int(input('Choose a action: '))
                if choose_methods <= len(obj) or choose_methods > 0: 
                    obj[choose_methods]()
                else:
                    print('INVALID RANGE')

ClientInterface().start_client()
