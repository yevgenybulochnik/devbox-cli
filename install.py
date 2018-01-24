#!/usr/bin/env python3
import os
import subprocess
import os.path as p
import datetime

SCRIPT_DIR = p.dirname(p.abspath(__file__))
SETUP_DIR = p.join(SCRIPT_DIR, 'setup')
LOG_DIR = p.join(SCRIPT_DIR, 'logs')

os.makedirs(SETUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

class dv_command:
    stamps = []
    def __init__(self, cmd_name, path=SCRIPT_DIR, type='sh'):
        self.cmd= cmd_name
        self.path = path
        self.type = type
    def run(self):
        self.time_logger(self.cmd)
        if self.type == 'py':
            self.logger(self.cmd)
            exec(self.cmd)
        else:
            log = self.logger(self.cmd)
            proc = subprocess.Popen(
                self.cmd.split(),
                cwd=self.path,
                stdout=log,
                stderr=log
            )
            proc.wait()
    def logger(self, command):
        command = command.split()
        if command[0] == 'sudo':
            command = command[1]
        else:
            command = command[0]
        spacer = '-' * 20
        log = open(p.join(LOG_DIR, 'dv_init.log'), 'a')
        log.write('\n' + spacer + command + spacer + '\n')
        log.flush()
        return log
    def time_logger(self, command):
        command = command.split()
        time_stamp = datetime.datetime.now()
        time_stamp_str = time_stamp.strftime('%m/%d/%y-%H:%M:%S:%f')
        if command[0] == 'sudo':
            command = command[1]
        else:
            command = command[0]
        spacer = '\n' + ('-' * 40) + '\n'
        log = open(p.join(LOG_DIR, 'dv_init_time.log'), 'a')
        log.write(spacer + command + '\n----' +  time_stamp_str + '\n')
        log.flush()
        self.stamps.append(time_stamp)



commands = [
    dv_command('wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -N', SETUP_DIR),
    dv_command('tar -xf Python-3.6.3.tgz', SETUP_DIR),
    dv_command(p.join('.', SETUP_DIR,'Python-3.6.3', 'configure'), SETUP_DIR),
    dv_command('rm -rf ' + SETUP_DIR),
    dv_command('print("Finish")', type='py')
]

for cmd in commands:
    cmd.run()

stamps = commands[0].stamps
start = stamps[0]
end = stamps[len(stamps) - 1]
print(str(end - start))
