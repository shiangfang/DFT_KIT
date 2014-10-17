
import sys, os, signal, errno
import subprocess

#save to pictures




#XMGRACE
class xm_grace:
    def __init__(self, fname='', printname='' , bufsize=-1, ask=None):
        if fname == '':
            cmd = ('xmgrace','-free',)
        else:
            cmd = ('xmgrace', fname ,'-free',)
            
        if printname is not '':
            cmd = cmd + ('-nosafe','-hdevice','EPS','-printfile',printname,)
            
        if ask is None:
            cmd = cmd + ('-noask',)

        self.commands=[]
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

        # Make the pipe that will be used for communication:
        (fd_r, fd_w) = os.pipe()
        cmd = cmd + ('-dpipe', `fd_r`)

        # Fork the subprocess that will start grace:
        self.pid = os.fork()

        if self.pid == 0:
            os.execvp('xmgrace', cmd)

        os.close(fd_r)
        self.pipe = os.fdopen(fd_w, 'w', bufsize)
        
    def add_command(self,cmd):
        self.commands.append(cmd)

    def run_commands(self,stop_=False):
        for cmd in self.commands:
            self.pipe.write(cmd+'\n')
        self.commands=[]
        if stop_:
            self.exit()

    def run(self, cmd):
        self.pipe.write(cmd + '\n')
        
    def flush(self):
        self.pipe.flush()


    def exit(self):
        self.run_cmd('exit')


#GNUplot

class gnu_plot:
    def __init__(self):
        self.proc=None
        self.commands=[]
        self.proc = subprocess.Popen(['gnuplot','-p'],shell=True,stdin=subprocess.PIPE)
        
    def add_command(self,cmd):
        self.commands.append(cmd)

    def run_commands(self,stop_=False):
        for cmd in self.commands:
            self.proc.stdin.write(cmd+'\n')
        self.commands=[]
        if stop_:
            self.exit()
            
    def run(self,cmd):
        self.proc.stdin.write(cmd+'\n')
            
    def exit(self):
        self.proc.stdin.write('quit\n') #close the gnuplot window
        
        

            
            