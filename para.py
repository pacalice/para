import paramiko
import os


class Targets:
    class TargetTypes:
        Person = 0
        Computer = 1
    Type = None
    Name = None

class SSHSessions:
    Sessions = {}
    class SSH:        
        client = paramiko.SSHClient()
        sshKey = None
        stderr = None
        stdout = None
        paswd = None
        stdin = None
        name = None
        host = None
        user = None
        keypath = None 
        IsConnected = False        

        def __init__(self,name="",host="",user="",paswd="",keypath=""):
            self.name = name
            self.host = host
            self.user = user
            self.paswd = paswd
            self.keypath = keypath
            if keypath != "":
                if os.path.exists(self.keypath):
                    self.sshKey = paramiko.RSAKey.from_private_key_file(self.keypath)

        def connect(self, name="",host="",user="",paswd="",keypath="", autoadd=True):
            if autoadd: self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.sshKey != None:
                self.client.connect(self.host, username=self.user, pkey=self.sshKey)
            else:
                try:                
                    self.client.connect(hostname=self.host, username=self.user, password=self.paswd)
                except Exception as ex:
                    print(f"{ex}")
                    return False
            self.IsConnected = True
            return True

        def execute(self, cmd, timeout=None, env=None):
            try:
                self.stdin,self.stdout,self.stderr = self.client.exec_command(command=cmd,timeout=timeout,environment=env)
            except Exception as ex:
                return str(ex)
            return self.stdout.readlines() # return lines as string with \n

        def disconnect(self):
            self.client.close()
            self.IsConnected = False

    def Connect(self,name="",host="",user="",paswd="",keypath="",autoadd=True):
        session = self.SSH(name=name, host=host, user=user, paswd=paswd, keypath=keypath)
        self.Sessions.update({name: session})
        return session.connect(name, host, user, paswd, keypath, autoadd)

    def Disconnect(self,name):
        session = self.Sessions.get(name)
        session.disconnect()
    
    def Delete(self,name):
        session = self.Sessions.get(name)
        session.pop(name)

    def Execute(self, name, cmd, timeout=None, env=None):
        session = self.Sessions.get(name)
        return session.execute(cmd, timeout=timeout, env=env)

    def IsConnected(self, name):
        session = self.Sessions.get(name)
        return session.IsConnected

    def List(self):
        return self.Sessions

    
sessions = SSHSessions()
for x in range(5):
    print(f"Connecting[{x}]: {sessions.Connect(f'dev{x}','172.16.117.141', 'pac', 'pac')}")
    print(f"Connected[{x}]: {sessions.IsConnected(f'dev{x}')}")
for x in range(5):
    sessions.Disconnect(f'dev{x}')
    print(f"Connected[{x}]: {sessions.IsConnected(f'dev{x}')}")

