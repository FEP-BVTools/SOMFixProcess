import sys
import glob
import serial
 
#取得目前可使用的COM Port
def serial_ports():
    """ Lists serial port names
 
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
 
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class SerialCtrl:
    def __init__(self):
        try:
            #連接獲取的第一個COM Port
            print("已連接", serial_ports()[0])
            self.ser=serial.Serial(serial_ports()[0],115200,timeout=0.5)

        except:
            print('COM連接失敗')
            exit()

    def GetDebugInfo(self):
        data = self.ser.readline().decode("big5")
        print(data,end='')

        return data

    def SerialClose(self):
        self.ser.close()
        print("已關閉COM port")

    def SerialWrite(self,words):
        self.ser.write(words)
        self.ser.flush()


 
if __name__ == '__main__':
    ser=SerialCtrl()
    print("----")
    for x in range(500):
        a=ser.GetDebugInfo()

    ser.SerialClose()
