import serial, time

text = {
    'textsent':404,
    'textmsg':'consulta'
}

num=text["textsent"]
msg=text["textmsg"]

strN="AT+CMGS=\"%s\"\r\n"%(num)
strNum=(strN.encode('ASCII'))
encoding='utf-8'

class TextMessage(object):
    def _ini_(self):
        self.connectPhone()
        self.initMessage()
    
    def connectPhone(self):
        self.phone=serial.Serial("/dev/ttyAMA0",115200,timeout=5)

    def initMessage(self):
        self.phone.write(b'AT+CMGF=1\r\n')
    
    def sendMessage(self):
        self.phone.write(strNum)
        print("Numero: "+str(num))
        self.confTime(1)
        print("Mensaje: "+msg)
        self.phone.write(msg.encode()+b"\r\n")
        self.confTime(1)
        self.phone.write(bytes([26]))
        self.confTime(0)
        print("Texto enviado\r\n")

    def getMessage(self):
        self.phone.write(b'AT+CMGL="REC READ"\r\n')
        self.confTime(1)
        datos=self.phone.readall()
        datos=str(datos,encoding)
        init=datos.find("+CMT:")
        init=init+6
        print("Recibio el SMS:")
        print(datos[init,len(datos)])

    def confTime(self,n):
        if n==1:
            time.sleep(0.5)
        else:
            time.sleep(1)
    
    def disconnectPhone(self):
        self.phone.close()

sms=TextMessage()
sms.connectPhone()
sms.sendMessage()
sms.getMessage()
sms.disconnectPhone()