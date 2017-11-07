# coding = utf-8
import traceback
import subprocess


def try_catch(func_do):
    def func(*args, **keyargs):
        try:
            return func_do(*args, **keyargs)
        except:
            print('Error execute: %s' % func_do.__name__)
            traceback.print_exc()
    return func


class Common:
    @staticmethod
    @try_catch
    def exe_shell(cmd):
        pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        pro = pro.communicate()
        if (pro[1] is None) and (pro[0] is not None):
            return pro[0]
        elif (pro[1] is not None) and (pro[0] is None):
            return pro[1]
        elif (pro[1] is not None) and (pro[0] is not None):
            return "%s\n%s" % (pro[0], pro[1])
        else:
            return None

    @classmethod
    def install_rpm(cls, path):
        msg = ""
        msg = cls.exe_shell("rpm -ivh %s" % path)
        return msg
