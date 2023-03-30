# mediapipe-live2d

## 目标
根据用户的面部动作生成同步的虚拟形象，并生成虚拟摄像头。

## 算法思路
与`mediapipe-anime`基本相同，将虚拟形象部分替换为unity+live2d \
目前在视频流和面部捕捉等方面的实现方式仍需优化改进。

**面部捕捉**：同样使用mediapipe获取面部关键点信息。\
**数据处理**：面部旋转角度的计算方式更改为通过与预保存的标准姿态模型进行比照计算，准确度和稳定性更高。暂未设置瞳孔位置、眉毛形态以及微笑状态的识别。\
**虚拟形象**：使用unity加载live2d模型，通过c#脚本和socket同步参数。目前的模型为Hiyori-free，后续可以增加新的模型或更改视频背景。unity组件位于unity\目录中。\
**软件集成**：使用pyinstaller打包为可执行项目文件。

## live2d
`Cubism` sdk for unity下载地址：[here](https://www.live2d.com/en/download/cubism-sdk/download-unity/) \
人物模型下载地址：[here](https://www.live2d.com/download/sample-data/) \
本项目的unity组件是集成了Cubism与Hiyori-free模型的完整程序，若仅使用目前模型则无需下载。

## 使用方法
集成好的可执行项目文件下载地址：[here](https://jbox.sjtu.edu.cn/l/I18aDS) （交大云盘）\
与`mediapipe-anime`相同，启动程序后，会自动创建名为`VirtualCamera`的虚拟摄像头，若视频仍无法正常显示，则需要手动运行/vc/Install.bat \
也可通过`pyinstaller`打包：
```
pip install pyinstaller
pyinstaller -D -w -n "mediapipe-live2d" -i logo.ico main.py --add-data "[虚拟环境路径]\Lib\site-packages\mediapipe\modules;mediapipe\modules" --add-data ".\vc;vc" --add-data ".\unity;unity" --add-data ".\model.dat;."
```
可在web端启动mediapipe-live2d.exe，然后调用虚拟摄像头`VirtualCamera`

## 依赖
Python >= 3.8 \
mediapipe >= 0.8.10.1 \
numpy >= 1.19.2 \
pyvirtualcam >= 0.9.1 \
opencv-python == 4.5.1.48 （大于此版本可能会导致pyinstaller不兼容）

## 参考
`VTuber Python Unity`：[here](https://github.com/mmmmmm44/VTuber-Python-Unity) \
mediapipe的使用方法，面捕算法的面部旋转角度计算以及unity模型的anime controller脚本参考以上项目完成。
