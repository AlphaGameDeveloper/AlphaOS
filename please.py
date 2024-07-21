import hashlib
import time
import whiptail
import system


class PleaseManager:
    def __init__(self):
        self.w = whiptail.Whiptail(title="Please authenticate", backtitle="DamienOS build {0}".format(
            open("/buildct").read().replace("\n", "")))
        self.hasher = hashlib.sha256()
        # self.hasher.update(bytes(time.ctime(), "utf-8"))
        # self.bootid = self.hasher.hexdigest()

    def attempt(self, ctx, args):
        del args[0]
        passwd = self.w.inputbox("Enter your password:", password=True)[0]
        print('password: "{0}"'.format(password))
        self.hasher.update(bytes(password, "utf-8"))
        if self.hasher.hexdigest() == bytes(
                system.data.get("main/password-sha256"), 'utf-8'):
            print("OK")
            with open("/.please-success", 'wb') as f:
                f.write(self.hasher.hexdigest())
        else:
            print("NOT OK")


manager = PleaseManager()
# manager.attempt()
