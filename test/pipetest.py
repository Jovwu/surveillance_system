# 主进程写，子进程读

from multiprocessing import Pipe, Process


from PyQt5.QtGui import QImage


from PIL import Image
import numpy as np
# im = Image.open("/home/lw/a.jpg")
# im.show()
# img = np.array(im)      # image类 转 numpy
# img = img[:,:,0]        #第1通道
# im=Image.fromarray(img) # numpy 转 image类
# im.show()


def func(out_pipe, in_pipe):
    in_pipe.close()
    # 关闭复制过来的管道的输入端
    while True:
        try:
            msg = out_pipe.recv()  # 子进程的管道端口接收主进程的数据

            im = Image.fromarray(msg)
            im.show()
        except EOFError:
            out_pipe.close()
            break


if __name__ == '__main__':
    out_pipe, in_pipe = Pipe()
    Process(target=func, args=(out_pipe, in_pipe)).start()  # 启动子进程
    out_pipe.close()  # 关闭主进程的输出管道端口

    im = Image.open("C:\zhongshiyu\WorkSpace\PythonProjects\pythonProject\image\奥巴马1.png")
    img = np.array(im)
    img = img[:,:,0]


    # for i in range(20):
    q = QImage()
    in_pipe.send(img)
        # 通过管道的端口向子进程写入
    in_pipe.close()

