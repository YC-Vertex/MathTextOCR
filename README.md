# MathTextOCR

## 环境和依赖

### Python环境

Python 3.7+

Python包：baidu-aip、PyQt5、pyautogui、numpy、opencv-python

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple baidu-aip PtQt5 pyautogui numpy opencv-python --user
```

### Mathpix Snipping Tool软件设置

1. 打开Mathpix Snipping Tool，将截图快捷键改为`CTRL+ALT+M`（默认）
2. 随便截一张图，并点击下方四个结果中第二个结果右侧的“复制到剪贴板”图标，此时第二个结果被设置为默认拷贝到剪贴板的结果

### 百度AI的API账号设置

1. 打开百度AI主页https://ai.baidu.com/
2. 点击右上角控制台，注册登录后点击左侧产品服务-文字识别
3. 点击创建应用，填写信息后点击立即创建。
4. 点击左侧应用列表，将其中的AppID、API Key、Secret Key三项分别拷贝至文件`MathTextOCR_Beta.py`中`APP_ID`、`API_KEY`、`SECRET_KEY`三个变量的单引号中。

## 使用MathTextOCR

1. 打开Mathpix Snipping Tool
2. 运行MathTextOCR：`python3 MathTextOCR_Beta.py`
3. 在Hotkey输入栏里输入快捷键，默认为's'，请确保快捷键是单个字符
4. 点击打开文件，选择需要识别的图片
5. 点击OK，打开框选界面
6. 键盘点击在（3）中设置的Hotkey
7. 在公式区域的左上角按下鼠标左键，拖动鼠标至公式区的右下角时松开，完成一次区域选取
8. 重复（6）（7），并且保证公式区域选取必须满足从下至上、从右至左的顺序
9. 按下回车键，开始进行转换
10. 转换结果会自动保存在在output.txt文件中

## 其它说明

只作为Demo，非完整版，有很多功能没有加入
