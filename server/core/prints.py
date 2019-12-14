def print_correct(msg):
    print('\033[32;1m %s \033[0m' % msg)

def print_error(msg):
    print('\033[31;1m %s \033[0m' % msg)

def exit_msg(msg):
    exit('\033[31;1m %s \033[0m' % msg)