import os
#个人测试用logger，把想要保存下来的log都打在目标文件里
def logger(data,name='logger',path='D:/logger'):
    os.makedirs(path)
    with open(path+'/'+name+'.txt','a')as f:
        f.writelines([data])
        f.write('\r\n')

