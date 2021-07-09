# RBS-Software
RBS is a toolbox software used in education industry
RBS 是一个应用于教育行业的工具箱软件

# Important issues 重要事项
- The author's native language is Chinese. All the following English descriptions are generated by translation software. Please forgive me for any mistakes
- 作者的母语是中文,以下所有英文描述全部为翻译软件生成,如有错误请原谅
# journal 日志
['2021/07/03', 'Ver021.07.03']

+改进:

1.主界面左上角图标现在可以正常显示

2.主界面现在支持文件拖拽

3.主界面GUI优化,修复BUG

4.添加两个临时功能模块,完成度20%(没有明显提示,但你仍可以打开它)

5.主界面"USER"模块已经完成

6.'随机数生成器'已经重写

-问题:

1.在线更新模块仍不可用

2.'下载器'模块完全无法使用

3.右侧侧边栏优化未完成

4.部分API接口未完成

5.'值日表'模块存在一个已知的恶性BUG

||信息:

ALL:129MB

DIST:37.4MB

ZIP:26.7MB

NSIS:25.6MB

-------------------------------------------------
['2021/06/02', 'Ver021.06.02']

+改进:

1.主界面添加左侧侧边栏

2.左侧侧边栏加入'HOME'功能,可一键回到主界面

3.分区'通用'中,模块'计时器'的BUG已修复,并重写了GUI,添加了停止功能

4.分区'化学'中,模块'元素周期表'已完成第四周期的数据录入

5.引导程序下方进度条逻辑修改

6.主界面的颜色主题已更换,改进标签的识别程度

7.分区'语文'中,添加了模块'成语接龙'

8.分区'信息'中,添加了模块'DDT'

9.主界面顶部的工具模块在光标经过时将显示正确的颜色

-问题:

1.在线更新模块仍不可用

2.'下载器'模块BUG未修复

3.右侧侧边栏不可用

||信息:

ALL:189MB

DIST:39.5MB

ZIP:28.8MB

NSIS:28.8MB

-------------------------------------------------
['2021/5/29', 'Ver021.05.29']

+改进:

1.主界面优化

2.化学-'化学配平'模块已取消

3.重写了'计时器'模块的代码,现在意外退出不再卡退

4.'值日表'模块现在可以自动获取桌面背景

5.修复了启动界面的进度条BUG

6.将语文-'简繁转化'模块的语料库加入文件验证列表

-问题:

1.在线更新模块仍不可用

2.'下载器'模块BUG未修复

||信息:

ALL:186MB

DIST:36.4MB

ZIP:29.1MB

NSIS:28.1MB

-------------------------------------------------
['2021/5/15', 'Ver021.05.15']

+改进:

1.添加模块'简繁体转换'属于语文类别

2.将'政治'分类移除,更改为'信息'

3.添加模块'下载器'属于信息类别

4.添加模块'PPT保存为图片'属于信息类别

5.添加模块'BMI计算'属于信息类别

6.主界面底端优化,增加提示标签

-问题:

1.在线更新模块仍不可用

2.'化学配平'模块仍不能使用

3.'下载器'模块有严重BUG,只能在网络良好时使用

||信息:

总大小:268MB

编译后大小:68.9MB

压缩后大小:50.8MB

-------------------------------------------------
['2021/5/01', 'Ver021.05.01']

+改进:

1.主程序添加了Log输出功能,负责收集并记录变量的变动信息

2.修复了hashlib的BUG,现在'校验文件完整性'功能已启用

3.'关于'模块的少量更改

4.缺少的功能将显示为NONE

5.编译打包时将启用UPX和密文加密

-问题:

1.在线更新模块仍不可用

2.更新和'化学配平'模块仍不能使用

||信息:

总大小:190MB

编译后大小:54.2MB

压缩后大小:36.0MB

-------------------------------------------------
['2021/4/18', 'Ver021.04.18']

+改进:

1.主程序界面优化

2.'值日表'模块已更新至V2,添加了手动模式,修复了一些BUG

3.添加了'基因库'模块,属于'生物'分类

4.启动器界面优化

5.字体调用的BUG已修复

6.字体'黑体'已本地化

-问题:

1.主界面GUI仍未处理完成

2.缺少模块的图标

3.更新和'化学配平'模块仍不能使用

||信息:

总大小:167MB

编译后大小:71.6MB

压缩后大小:29.5MB

-------------------------------------------------
['2021/3/27', 'Ver021.03.27']

+改进:

1.按照学科分类的GUI

2.增加了不同的颜色主题

3.将顶部工具栏全部转化为图标(可节省空间)

4.更新了启动器的GUI和库文件加载逻辑

-问题:

1.需要更多的功能模块

2.分类器已被完全禁用,因为生成EXE时不能正常工作.

3.启动器使用的字体丢失

||信息:

编译前大小:44.6MB

编译后大小:46.9MB

压缩后大小:15.5MB

-------------------------------------------------
['2021/3/13', 'Ver021.03.13']

+改进:

1.新,中文语法分析器

2.'进制转换器'添加了8进制转换

3.修复了'进制转换器'中,输入框光标丢失的问题.

4.'进制转换器'在无文本情况下运算不再报错.

5.名单册构建已完成

6.新的图标已完成(并不是最好的)

7.中文语料库本地化

8.主程序添加了'更新日志功能'

9.Visual Studio 2010编译文件本地化(msvcr100.dll)理论支持win7

-问题:

1.禁用了WALP_Engine,因为它工作不稳定

2.将WX_Engine从计划列表中删除

3.python平台从3.9.1降级到3.8.8,因为缺少库的支持.

4.'中文语法分析器'60％的功能被禁用，因为它在打包到EXE时失败了．

||信息:

编译前大小:38.3MB

编译后大小:440MB

压缩后大小:99.6MB
