import os

from Crypto.Cipher import AES
from binascii import a2b_hex
import uuid


############################ 检查权限 #############################
class Get_License(object):
    def __init__(self):
        super(Get_License, self).__init__()

        # 定义秘钥信息
        self.seperateKey = "ylkj8702"
        # self.seperateKey = "d#~0^38J:"
        self.aesKey = "123456789abcdefg"
        self.aesIv = "abcdefg123456789"
        self.aesMode = AES.MODE_CBC

    # def getHwAddr(self, ifname):
    #     """
    #     获取主机物理地址
    #     """
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    #     return ''.join(['%02x' % ord(char) for char in info[18:24]])
    def getHwAddr(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def decrypt(self, text):
        """
        从.lic中解密出主机地址
        """
        try:
            cryptor = AES.new(self.aesKey, self.aesMode, self.aesIv)

            plain_text = cryptor.decrypt(a2b_hex(text))
            # print(plain_text.decode('utf-8').rstrip('0'))
            # exit()
            return plain_text.decode('utf-8').rstrip('0')
        except:
            return "错了"

    def getLicenseInfo(self, filePath=None):
        if filePath == None:
            # filePath = "/license.lic"
            filePath = os.getcwd()+"/license.lic"

        if not os.path.isfile(filePath):
            print("请将 license.lic 文件放在当前路径下")
            os._exit(0)
            return False, 'Invalid'

        encryptText = ""
        with open(filePath, "rb") as licFile:
            encryptText = licFile.read()
            licFile.close()
        try:
            hostInfo = self.getHwAddr()
        except IOError:
            hostInfo = self.getHwAddr()

        decryptText = self.decrypt(encryptText)
        pos = decryptText.find(self.seperateKey)

        if -1 == pos:
            return False, "Invalid"
        licHostInfo = self.decrypt(decryptText[0:pos])
        licenseStr = decryptText[pos + len(self.seperateKey):]

        import datetime
        exp_time = licHostInfo[:10]
        now = datetime.datetime.now()
        temp_now = now.strftime('%Y-%m-%d')
        now = datetime.datetime.strptime(temp_now, '%Y-%m-%d')

        future_time = datetime.datetime.strptime(exp_time, '%Y-%m-%d')

        res = future_time - now
        # print(licHostInfo[10:27])
        # print(hostInfo)
        # exit()
        if licHostInfo[10:27] == hostInfo and res.days > 0:
            print("*" * 100)
            print('您使用期限还有:', res.days, '天')
            print("*" * 100)

            return True, licenseStr
        else:
            return False, 'Invalid'
        # if res.days > 0:
        #     print("*" * 100)
        #     print('您使用期限还有:', res.days, '天')
        #     print("*" * 100)
        #
        #     return True, licenseStr
        # else:
        #     return False, 'Invalid'


#c8:69:cd:96:58:56
License = Get_License()
condition, LicInfo = License.getLicenseInfo()

class Today():
    def get_time(self):       
        if condition==True and LicInfo=='Valid':
            print(datetime.datetime.now())
        else:
            print('未权授！')

    def say(self):
        if condition==True and LicInfo=='Valid':
            print('hello world!')
        else:
            print('未权授！')

