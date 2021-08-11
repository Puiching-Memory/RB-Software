# -*- coding: utf-8 -*-

###########################################################################
# Power by ZK2021
# @Puiching Memory™
# python version: 3.8.10
#  ____  ____ ____       ____         __ _
# |  _ \| __ ) ___|     / ___|  ___  / _| |___      ____ _ _ __ ___
# | |_) |  _ \___ \ ____\___ \ / _ \| |_| __\ \ /\ / / _` | '__/ _ \
# |  _ <| |_) |__) |_____|__) | (_) |  _| |_ \ V  V / (_| | | |  __/
# |_| \_\____/____/     |____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|
#
###########################################################################
#
#	↓↓↓↓↓格式声明↓↓↓↓↓
#	1.开头使用两个##注释掉的代码可以正常运行,但因特别原因不再使用
#	2.使用一个#注释掉的为正常注释
#	3.少量注释中使用箭头↓等特殊字符,这可能指的是所指方向的一行或一个段落的代码
#
###########################################################################

# ↓↓↓↓↓ import ↓↓↓↓↓

# 功能库
import M_Roll # 随机数生成器
import M_Element # 元素周期表
import M_Pinyin # 中文转拼音
import M_Roster # 值日表
import M_Gene # 基因数据库
import M_About # 关于信息
import M_Pi # 圆周率计算器
import M_Capslook # 大小写转换
import M_Base_conversion # 十进制转换器
import M_Traditional_Chinese # 中文繁体简体互转
import M_BMI # BMI计算器
import M_PPTNG # PPT导出图片
import M_Download # 下载器
import M_Timer # 计时器
import M_PPT # PPT小工具
import M_Idion # 成语接龙
import M_DDT # '外挂'集合
import M_Music # 音乐分析器
import M_WALP # WALP地理信息系统
import M_Version # 版本查看器
import M_History # 历史上的今天
import M_Date # 日期查看器
import M_File # 文件管理器
import M_QRcode # 二维码生成器
import M_BingWallPaper # 必应壁纸

import WeaterAPI # 天气API

import User # 用户界面
import Setting # 设置界面
import Plug_in # 插件

# 临时库
import L_College
import YOLO

# 辅助功能库
import sys
import os
import win32com.client
import win32api
import psutil
import time
import ping3
import random
##import gc # 内存库

# 核心库
import wx
import wx.adv
import GUI
import configparser # 设置文件(.cfg)库
import logging.handlers # 日志库
import threading # 多线程

###########################################################################
# Class Main
###########################################################################


class CalcFrame(GUI.Main):

	# ↓↓↓↓↓ 定义wx.ID ↓↓↓↓↓
	MENU_EXIT   = wx.NewIdRef()

	def __init__(self, parent):
		GUI.Main.__init__(self, parent) # 初始化
		self.threads = []

		#↓↓↓↓↓ 定义全局变量 ↓↓↓↓↓
		global Main_State, FUN_State, version, setup, Colour_G, Hover, colour_Hover, last, cfg, screen_size_x,screen_size_y
		cfg = configparser.ConfigParser()  # 读取设置文件
		cfg.read('./cfg/main.cfg')
		last = cfg.get('History', 'LAST')
		Main_State = cfg.get('History', 'MAINSTATE')
		version = cfg.get('main', 'VERSION')
		transparent = cfg.get('main', 'transparent')
		is_exe = cfg.get('main', 'is_exe')
		screen_size_x = int(cfg.get('screen', 'size_x'))
		screen_size_y = int(cfg.get('screen', 'size_y'))
		Is_complete = cfg.get('Check', 'Is_complete')

		Log()  # 初始化LOG设置
		logging.debug('Document integrity check文件完整性检查:' + Is_complete)

		Self_CMD(self, '载入设置完成') # 向自定义控制台发送消息
		Self_CMD(self, '文件完整性检查:' + Is_complete)

		print('屏幕PPI值:' + str(wx.Display.GetPPI(wx.Display()))) # 信息收集
		print('屏幕分辨率:' + str(wx.ClientDisplayRect()))
		print('彩色模式:' + str(wx.ColourDisplay()))
		print('GUI大小:' + str(self.Size))


		setup = 0  # 初始化操作所用的变量,所有操作完成后会变成1
		FUN_State = 'NONE'
		Hover = 0  # 检测当前Hover的按钮是哪个
		colour_Hover = '#A65F00'  # 顶部按钮被Hover时呈现的颜色
		Colour_G = '#cccccc'  # 分区按钮Hover时呈现的颜色

		#------------------------------ 主界面初始化操作，设置文本常量,颜色值,按钮呈现等
		self.version.SetLabel('#V' + version) # 设置版本号

		if is_exe == 'True': # 主界面大小设置(针对打包后程序的调整)
			self.SetSize(screen_size_x - 10,screen_size_y - 10)
			screen_size_x = screen_size_x - 10
			screen_size_y = screen_size_y - 10
		else:
			self.SetSize(screen_size_x,screen_size_y)

		self.Weather.SetLabel(WeaterAPI.Now_weather()) # 获取and显示天气信息

		self.taskBar = wx.adv.TaskBarIcon() # 声明:启用系统托盘
		self.SetDoubleBuffered(True) # 声明:启用双缓冲
		self.SetDropTarget(FileDrop(self)) # 声明:接受文件拖放
		self.SetIcon(wx.Icon('ICOV4.ico', wx.BITMAP_TYPE_ICO)) # 设置GUI图标(左上角)

		''' 系统状态栏(弃用方案)
		self.Bar.SetStatusWidths([-5,-295,-5,-250,-5,-170]) #区域宽度比列
		self.Bar.SetStatusText(self.Space1.GetLabel(), 0)
		self.Bar.SetStatusText(self.Bottom_Bar1.GetLabel(), 1)
		self.Bar.SetStatusText(self.Space2.GetLabel(), 2)
		self.Bar.SetStatusText(self.Bottom_Bar2.GetLabel(), 3)
		self.Bar.SetStatusText(self.Space3.GetLabel(), 4)
		self.Bar.SetStatusText(self.Bottom_Bar3.GetLabel(), 5)
		##self.Bar.SetStatusStyles(self, 1)
		'''
		start(self)  # 初始化界面布局函数(纯操作,无计算)

		if last != 'NONE':
			self.Fast.SetLabel(last)

		if Main_State == 'NONE':
			Main_State = 0

		if cfg.get('History', 'COLOR') != 'NONE' and tuple(eval(cfg.get('History', 'COLOR'))) != (255, 255, 255, 255):
			self.Fast.SetBackgroundColour(
				wx.Colour(tuple(eval(cfg.get('History', 'COLOR')))))

		self.SetTransparent(int(transparent)) # 设置窗口透明度
		##self.SetCursor(wx.Cursor(6)) # 设置窗口光标

		# 初始化完成后日志输出
		logging.debug(str('Initialization complete初始化完成:' +
						  time.strftime('%Y/%m/%d*%H:%M:%S')))
		logging.debug('Version软件版本:' + version)

		Self_CMD(self, '初始化完成,日志已保存')

	def Sacc(self, event):
		'''
		主界面背景图片绘制
		'''
		if setup == 1:
			dc = event.GetDC()
			dc.DrawBitmap(wx.Bitmap("./pictures/Background.jpg"), 0, 0)
			##print(1)
		else:
			dc = event.GetDC()
			dc.Clear()


	def Close(self, event):
		'''
		windows_关闭程序
		'''
		while self.threads: # 移除其他线程
			thread = self.threads[0]
			thread.timeToQuit.set()
			self.threads.remove(thread)

		if self.taskBar.IsAvailable == True: # 移除托盘图标
			self.taskBar.RemoveIcon()

		cfg.read('./cfg/main.cfg')
		cfg.set('History', 'LAST', FUN_State)
		cfg.set('History', 'MAINSTATE', str(Main_State))
		cfg.set('History', 'COLOR', str(
			self.Bottom_Bar1.GetBackgroundColour()))
		cfg.write(open('./cfg/main.cfg', 'w'))
		# 日志输出
		logging.debug(
			str('windows quit:' + time.strftime('%Y/%m/%d*%H:%M:%S')))
		# 关闭程序
		wx.CallAfter(sys.exit, 0)

	def Quit(self, event):
		'''
		self_关闭程序
		'''
		while self.threads: # 移除其他线程
			thread = self.threads[0]
			thread.timeToQuit.set()
			self.threads.remove(thread)

		if self.taskBar.IsAvailable == True: # 移除托盘图标
			self.taskBar.RemoveIcon()

		cfg.read('./cfg/main.cfg')
		cfg.set('History', 'LAST', FUN_State)
		cfg.set('History', 'MAINSTATE', str(Main_State))
		cfg.set('History', 'COLOR', str(
			self.Bottom_Bar1.GetBackgroundColour()))
		cfg.write(open('./cfg/main.cfg', 'w'))
		# 日志输出
		logging.debug(str('self quit:' + time.strftime('%Y/%m/%d*%H:%M:%S')))
		# 关闭程序
		wx.CallAfter(self.Destroy)

	def Ico(self, event):
		'''
		窗口最小化-事件触发
		'''
		print('窗口最小化:' + str(self.IsIconized()))
		if self.IsIconized() == True:
			self.Enable(False)
			'''
			# 释放内存的一种方法,在这里不适用
			del self # 删除变量
			gc.collect() # 调用GC库释放内存
			'''
			self.Net_Timer.Stop()
			self.PFM_Timer.Stop()
			self.PRAM_Timer.Stop()
			self.PRO_Timer.Stop()
			self.Time_Timer.Stop()

			self.taskBar.SetIcon(wx.Icon(os.path.join("./ICOV4.ico"), wx.BITMAP_TYPE_ICO), "RBS_Software2021") # 设置系统托盘图标

			self.taskBar.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnTaskBar) # 右键单击托盘图标
			##self.taskBar.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnTaskBar) # 左键单击托盘图标
			##self.taskBar.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBar) # 左键双击托盘图标
			##self.taskBar.Bind(wx.EVT_MENU, self.OnShow, id=self.MENU_SHOW) # 显示窗口
			##self.taskBar.Bind(wx.EVT_MENU, self.OnHide, id=self.MENU_HIDE) # 隐藏窗口
			##self.taskBar.Bind(wx.EVT_MENU, self.OnOpenFolder, id=self.MENU_FOLFER) # 打开输出目录
			##self.taskBar.Bind(wx.EVT_MENU, self.OnConfig, id=self.MENU_CONFIG) # 设置
			self.taskBar.Bind(wx.EVT_MENU, self.Close, id=self.MENU_EXIT) # 退出


		else:
			self.Enable(True)
			self.Net_Timer.Start(10000)
			self.PFM_Timer.Start(3000)
			self.PRAM_Timer.Start(60000)
			self.PRO_Timer.Start(3000)
			self.Time_Timer.Start(900)

			self.taskBar.RemoveIcon()

	def Cmd(self, event):
		# 打开Cmd
		os.system("C:\WINDOWS\system32\cmd.exe")

	def About(self, event):
		# 打开<关于>界面
		M_About.main()

	def Log(self, event):
		# 更新日志
		M_Version.main()

	def Setting(self, event):
		# 打开设置
		Setting.main()

	def Update(self, event):
		# 打开<联网更新>界面
		if proc_exist('Update.exe'):
			print('程序已运行')
		else:
			wx.CallAfter(win32api.ShellExecute, 0, 'open', 'Update.exe', '','',1)


	def File(self, event):
		M_File.main()

	def HOME(self, event):
		''' 返回主界面 '''
		Home(self)

	def Plug_in(self, event):
		Plug_in.main()

	def User(self, event):
		User.main()

	def LLL(self, event):
		L_College.main()

	def GetWeather(self, event):
		self.Weather.Enable(False)
		self.Weather.SetLabel(WeaterAPI.Now_weather())
		print('获取天气信息...')
		self.Weather.Enable(True)

	def CMD_Enter(self, event):
		CMD(self, self.CMD_IN.GetValue())
		self.CMD_IN.SetValue('')

	def move_start(self, frame_pos):
		##print(random.random())
		self.SetPosition(frame_pos)
	

	def OnLeftDown(self, event):
		thread = WorkerThread(self)
		self.threads.append(thread)
		thread.start()

	def OnLeftUp(self, event):
		if self.threads:
			self.threads[0].timeToQuit.set()
			self.threads.remove(self.threads[0])


	def OnTaskBar(self, event):
		'''
		系统托盘图标_对应操作
		'''
		menu = wx.Menu()
		menu.AppendSeparator()
		menu.Append(self.MENU_EXIT, "退出") # 使用系统托盘退出的方法会引发一个C++的错误,错误原因未知,解决方法未知,不会导致可见的问题

		self.taskBar.PopupMenu(menu) # 显示托盘菜单
		menu.Destroy() # 销毁托盘菜单

	def BT2(self, event):
		M_Date.main()

	def Fast_on(self, event):
		check_name = ['中文转拼音', '简-繁转换', '成语接龙', '', '圆周率', '', '', '', '大小写转换', '', '', '', '下载器', 'PPT出图', 'BMI', 'DDT', '',
					  '', '', '', '', '', '', '', '', '', '', '', '元素周期表', '', '', '', '基因库', '', '', '', '随机数生成器', '进制转换', '值日表', '计时器']
		into_program = [M_Pinyin, M_Traditional_Chinese, M_Idion, None, M_Pi, None, None, None, M_Capslook, None, None, None, M_Download, M_PPTNG, M_BMI, M_DDT, None, None,
						None, None, None, None, None, None, None, None, None, None, M_Element, None, None, None, M_Gene, None, None, None, M_Roll, M_Base_conversion, M_Roster, M_Timer]
		for (name, program) in zip(check_name, into_program):
			if name == self.Fast.GetLabel():
				program.main()

	# ---------------------------------------------------------------------

	def PFM_Tick(self, event):
		''' 计时器-性能监视器 '''
		global CPU_text, RAM_text # 定义全局变量
		Line1 = psutil.swap_memory()
		Line2 = psutil.cpu_times_percent()

		CPU_text = str(Line2.user) + "%"  # 合并字符串
		RAM_text = str(Line1.percent) + "%"

		self.Bottom_Bar3.SetLabel('CPU:' + CPU_text + '  RAM:' + RAM_text)


	def PRAM_Tick(self, event):
		'''
		计时器-内存监视器
		'''
		process_lst = []
		mem = 0
		try:
			for pid in psutil.pids():
				p = psutil.Process(pid)
				if (p.name() == 'RBS_Software2021.exe'):
					process_lst.append(p)

			for i in process_lst:
				##print(i.memory_info()[1] / 1024 / 1024)
				mem = mem + i.memory_info()[1] / 1024 / 1024

			self.Bottom_Bar4.SetLabel(str(round(mem)) + 'MB')
		except:
			self.Bottom_Bar4.SetLabel('--MB')


	def PRO_Tick(self, event):
		'''
		计时器-后台探针
		'''
		if proc_exist('POWERPNT.EXE'):
			##print('PPT is running')
			self.PPT_Timer.Stop()
			M_PPT.main()
		else:
			event.Skip()
			##print('no such process...')


	def Net_Tick(self, event):
		'''
		计时器-网络监视器
		'''
		try:
			ping = str(int(ping3.ping('www.baidu.com') * 1000))[0:3]
			if int(ping) == 0:
				self.Network.SetLabel('Net:Ero')
			else:
				self.Network.SetLabel('Net:' + ping + 'ms')
		except:
			self.Network.SetLabel('Net:Ero')


	def Time_Tick(self, event):
		'''
		计时器-时间显示
		'''
		self.Bottom_Bar2.SetLabel(time.strftime('%Y/%m/%d*%H:%M:%S'))

	# ------------------------------------------------------------------------

	def Hover1(self, event):
		''' 光标经过，接触到按钮时（功能按钮），改变提示标签文本 '''
		self.Bottom_Bar1.SetLabel('Function1')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 11

	def Hover2(self, event):
		self.Bottom_Bar1.SetLabel('Function2')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 12

	def Hover3(self, event):
		self.Bottom_Bar1.SetLabel('Function3')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 13

	def Hover4(self, event):
		self.Bottom_Bar1.SetLabel('Function4')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 14

	def Hover_L1(self, event):
		self.Side1.SetBackgroundColour(colour_Hover)
		self.Bottom_Bar1.SetLabel('Back to HOME')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 41

	def Hover_L2(self, event):
		self.Side2.SetBackgroundColour(colour_Hover)
		self.Bottom_Bar1.SetLabel('check the plug-in')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 42

	def Hover_L3(self, event):
		self.Side3.SetBackgroundColour(colour_Hover)
		self.Bottom_Bar1.SetLabel('login as user')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 43

	def Hover_L4(self, event):
		self.Side4.SetBackgroundColour(colour_Hover)
		self.Bottom_Bar1.SetLabel('Background service program')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 44

	def H_LOG(self, event):
		''' 顶部功能按钮提示 '''
		self.Bottom_Bar1.SetLabel('update log')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 31

		self.B_Log.SetBackgroundColour(colour_Hover)

	def H_SET(self, event):
		self.Bottom_Bar1.SetLabel('software setting')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 32

		self.B_Setting.SetBackgroundColour(colour_Hover)

	def H_ABO(self, event):
		self.Bottom_Bar1.SetLabel('About us')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 33

		self.B_About.SetBackgroundColour(colour_Hover)

	def H_CMD(self, event):
		self.Bottom_Bar1.SetLabel('open cmd on windows')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 34

		self.B_Cmd.SetBackgroundColour(colour_Hover)

	def H_UPD(self, event):
		self.Bottom_Bar1.SetLabel('check to update online')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 35

		self.B_Update.SetBackgroundColour(colour_Hover)

	def H_QUT(self, event):
		self.Bottom_Bar1.SetLabel('quit/end the software')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 36

		self.B_Quit.SetBackgroundColour(colour_Hover)

	def H_File(self, event):
		self.Bottom_Bar1.SetLabel('File manager')
		self.SetCursor(wx.Cursor(6))
		global Hover
		Hover = 37

		self.B_File.SetBackgroundColour(colour_Hover)

	def Class1(self, event):
		''' 光标经过，接触到按钮（分区按钮）时，改变提示标签文本 '''
		self.Bottom_Bar1.SetLabel(str('功能分区1--' + self.G1.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 1:
			event.Skip()
		else:
			self.G1.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 21

	def Class2(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区2--' + self.G2.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 2:
			event.Skip()
		else:
			self.G2.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 22

	def Class3(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区3--' + self.G3.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 3:
			event.Skip()
		else:
			self.G3.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 23

	def Class4(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区4--' + self.G4.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 4:
			event.Skip()
		else:
			self.G4.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 24

	def Class5(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区5--' + self.G5.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 5:
			event.Skip()
		else:
			self.G5.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 25

	def Class6(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区6--' + self.G6.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 6:
			event.Skip()
		else:
			self.G6.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 26

	def Class7(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区7--' + self.G7.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 7:
			event.Skip()
		else:
			self.G7.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 27

	def Class8(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区8--' + self.G8.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 8:
			event.Skip()
		else:
			self.G8.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 28

	def Class9(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区9--' + self.G9.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 9:
			event.Skip()
		else:
			self.G9.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 29

	def Class10(self, event):
		self.Bottom_Bar1.SetLabel(str('功能分区10--' + self.G10.GetLabel()))
		self.SetCursor(wx.Cursor(6))
		if Main_State == 10:
			event.Skip()
		else:
			self.G10.SetBackgroundColour(Colour_G)
		global Hover
		Hover = 210

	# ---------------------------------------------------------------------

	def Leave(self, event):
		''' 通用,离开事件 '''
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))

	def Leave1(self, event):
		''' 光标离开，不接触按钮时，改变提示标签文本 '''
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 1:
			event.Skip()
		else:
			self.G1.SetBackgroundColour('white')
			self.G1.SetForegroundColour('black')

	def Leave2(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 2:
			event.Skip()
		else:
			self.G2.SetBackgroundColour('white')
			self.G2.SetForegroundColour('black')

	def Leave3(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 3:
			event.Skip()
		else:
			self.G3.SetBackgroundColour('white')
			self.G3.SetForegroundColour('black')

	def Leave4(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 4:
			event.Skip()
		else:
			self.G4.SetBackgroundColour('white')
			self.G4.SetForegroundColour('black')

	def Leave5(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 5:
			event.Skip()
		else:
			self.G5.SetBackgroundColour('white')
			self.G5.SetForegroundColour('black')

	def Leave6(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 6:
			event.Skip()
		else:
			self.G6.SetBackgroundColour('white')
			self.G6.SetForegroundColour('black')

	def Leave7(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 7:
			event.Skip()
		else:
			self.G7.SetBackgroundColour('white')
			self.G7.SetForegroundColour('black')

	def Leave8(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 8:
			event.Skip()
		else:
			self.G8.SetBackgroundColour('white')
			self.G8.SetForegroundColour('black')

	def Leave9(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 9:
			event.Skip()
		else:
			self.G9.SetBackgroundColour('white')
			self.G9.SetForegroundColour('black')

	def Leave10(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		if Main_State == 10:
			event.Skip()
		else:
			self.G10.SetBackgroundColour('white')
			self.G10.SetForegroundColour('black')

	def Leave_L1(self, event):
		self.Side1.SetBackgroundColour(colour_SideL)
		self.SetCursor(wx.Cursor(1))

	def Leave_L2(self, event):
		self.Side2.SetBackgroundColour(colour_SideL)
		self.SetCursor(wx.Cursor(1))

	def Leave_L3(self, event):
		self.Side3.SetBackgroundColour(colour_SideL)
		self.SetCursor(wx.Cursor(1))

	def Leave_L4(self, event):
		self.Side4.SetBackgroundColour(colour_SideL)
		self.SetCursor(wx.Cursor(1))

	def L_LOG(self, event):
		''' 顶部功能按钮提示 '''
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_Log.SetBackgroundColour(self.version.GetBackgroundColour())

	def L_SET(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_Setting.SetBackgroundColour(
			self.version.GetBackgroundColour())

	def L_ABO(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_About.SetBackgroundColour(
			self.version.GetBackgroundColour())

	def L_CMD(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_Cmd.SetBackgroundColour(self.version.GetBackgroundColour())

	def L_UPD(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_Update.SetBackgroundColour(
			self.version.GetBackgroundColour())

	def L_QUT(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_Quit.SetBackgroundColour(
			self.version.GetBackgroundColour())

	def L_File(self, event):
		self.Bottom_Bar1.SetLabel('Get focus to show prompts')
		self.SetCursor(wx.Cursor(1))
		self.B_File.SetBackgroundColour(self.version.GetBackgroundColour())

	# -----------------------------------------------------------------------

	def Function1(self, event):
		''' 点击事件_按钮1 '''
		global FUN_State
		FUN_State = self.T_F1.GetLabel()

		if Main_State == 1:
			M_Pinyin.main()
		elif Main_State == 2:
			M_Pi.main()
		elif Main_State == 3:
			M_Capslook.main()
		elif Main_State == 4:
			M_Download.main()
		elif Main_State == 5:
			M_History.main()
		elif Main_State == 6:
			M_WALP.main()
		elif Main_State == 7:
			M_Music.main()
		elif Main_State == 8:
			M_Element.main()
		elif Main_State == 9:
			M_Gene.main()
		elif Main_State == 10:
			M_Roll.main()

	def Function2(self, event):
		''' 点击事件_按钮2 '''
		global FUN_State
		FUN_State = self.T_F2.GetLabel()

		if Main_State == 1:
			M_Traditional_Chinese.main()
		elif Main_State == 2:
			return
		elif Main_State == 3:
			return
		elif Main_State == 4:
			M_PPTNG.main()
		elif Main_State == 5:
			M_BingWallPaper.main()
		elif Main_State == 6:
			return
		elif Main_State == 7:
			L_College.main()
		elif Main_State == 8:
			return
		elif Main_State == 9:
			return
		elif Main_State == 10:
			M_Base_conversion.main()

	def Function3(self, event):
		''' 点击事件_按钮3 '''
		global FUN_State
		FUN_State = self.T_F3.GetLabel()

		if Main_State == 1:
			M_Idion.main()
		elif Main_State == 2:
			return
		elif Main_State == 3:
			return
		elif Main_State == 4:
			M_BMI.main()
		elif Main_State == 5:
			return
		elif Main_State == 6:
			return
		elif Main_State == 7:
			M_QRcode.main()
		elif Main_State == 8:
			return
		elif Main_State == 9:
			return
		elif Main_State == 10:
			M_Roster.main()

	def Function4(self, event):
		''' 点击事件_按钮4 '''
		global FUN_State
		FUN_State = self.T_F4.GetLabel()
		if Main_State == 1:
			return
		elif Main_State == 2:
			return
		elif Main_State == 3:
			return
		elif Main_State == 4:
			M_DDT.main()
		elif Main_State == 5:
			return
		elif Main_State == 6:
			return
		elif Main_State == 7:
			YOLO.video_demo()
		elif Main_State == 8:
			return
		elif Main_State == 9:
			return
		elif Main_State == 10:
			M_Timer.main()

	# --------------------------------------------------------------------

	def G_1(self, event):
		''' 1号功能分区-语文 '''

		global Main_State, colour_Hover, colour_SideL  # 定义(全局)状态变量
		Main_State = 1

		Colour_clean(self)  # 清空所有颜色

		start(self)

		colour_cfg = configparser.ConfigParser() # 主界面颜色定义
		colour_cfg.read('./DATA/Main/Theme/colourful/Page1.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note1.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1) # 随机抽取一条
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)  # 主界面颜色设置

		self.G1.SetBackgroundColour(colour_Main)  # 主界面颜色设置
		self.G1.SetForegroundColour("White")  # 按钮字体颜色设置

		self.T_F1.SetLabel("中文转拼音")  # 设置功能按钮的标签
		self.T_F2.SetLabel("简-繁转换")
		self.T_F3.SetLabel("成语接龙")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('将输入的中文转化为拼音,支持多音字')
		self.Tip2.SetLabel('如题,将中文简体和繁体字互相转换')
		self.Tip3.SetLabel('拥有一万对成语的接龙,你能顶得住吗?')
		self.Tip4.SetLabel('什么都没有呢!')

		# 功能主标题下方的四个按钮的设置(每四个一组,网络,文件)
		Function_icon(self, 0, 0, 0, 0, 1, 1, 1, 0)

		self.Refresh()  # 刷新屏幕

	def G_2(self, event):
		''' 2号功能分区-数学 '''
		global Main_State, colour_Hover, colour_SideL
		Main_State = 2

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page2.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note2.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G2.SetBackgroundColour(colour_Main)
		self.G2.SetForegroundColour("White")

		self.T_F1.SetLabel("圆周率")
		self.T_F2.SetLabel("NONE")
		self.T_F3.SetLabel("NONE")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('记录了小数点后一万位,支持本地解算')
		self.Tip2.SetLabel('什么都没有呢!')
		self.Tip3.SetLabel('什么都没有呢!')
		self.Tip4.SetLabel('什么都没有呢!')

		Function_icon(self, 0, 0, 0, 0, 1, 0, 0, 0)

		self.Refresh()

	def G_3(self, event):
		''' 3号功能分区-英语 '''

		global Main_State, colour_Hover, colour_SideL
		Main_State = 3

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page3.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')
		
		note = open('./DATA/Main/Note/Note3.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G3.SetBackgroundColour(colour_Main)
		self.G3.SetForegroundColour("White")

		self.T_F1.SetLabel("大小写转换")
		self.T_F2.SetLabel("NONE")
		self.T_F3.SetLabel("NONE")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('将所有英文字母在大写/小写中转换')
		self.Tip2.SetLabel('什么都没有呢!')
		self.Tip3.SetLabel('什么都没有呢!')
		self.Tip4.SetLabel('什么都没有呢!')

		Function_icon(self, 0, 0, 0, 0, 0, 0, 0, 0)

		self.Refresh()

	def G_4(self, event):
		''' 4号功能分区-信息 '''

		global Main_State, colour_Hover, colour_SideL
		Main_State = 4

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page4.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')
		
		note = open('./DATA/Main/Note/Note4.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')
		
		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G4.SetBackgroundColour(colour_Main)
		self.G4.SetForegroundColour("White")

		self.T_F1.SetLabel("下载器")
		self.T_F2.SetLabel("PPT出图")
		self.T_F3.SetLabel("BMI")
		self.T_F4.SetLabel("DDT")

		self.Tip1.SetLabel('单线程下载器,确保你输入的url是可用的!')
		self.Tip2.SetLabel('将选定文件夹内的所有PPT导出为图片')
		self.Tip3.SetLabel('BMI计算器,简单,易用,但没人关心这个')
		self.Tip4.SetLabel('(DDT)破环性实验功能，谨慎使用，任何造成的损失后果自负')

		Function_icon(self, 1, 0, 0, 1, 1, 1, 0, 0)

		self.Refresh()

	def G_5(self, event):
		''' 5号功能分区-历史 '''

		global Main_State, colour_Hover, colour_SideL
		Main_State = 5

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page5.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note5.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G5.SetBackgroundColour(colour_Main)
		self.G5.SetForegroundColour("White")

		self.T_F1.SetLabel("历史上的今天")
		self.T_F2.SetLabel("必应壁纸")
		self.T_F3.SetLabel("NONE")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('数据来自www.ipip5.com')
		self.Tip2.SetLabel('朋友,不知道用什么壁纸?来这找找吧')
		self.Tip3.SetLabel('什么都没有呢!')
		self.Tip4.SetLabel('什么都没有呢!')

		Function_icon(self, 0, 0, 0, 0, 0, 0, 0, 0)

		self.Refresh()

	def G_6(self, event):
		''' 6号功能分区-地理 '''
		global Main_State, colour_Hover, colour_SideL
		Main_State = 6

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page6.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note6.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G6.SetBackgroundColour(colour_Main)
		self.G6.SetForegroundColour("White")

		self.T_F1.SetLabel("WALP")
		self.T_F2.SetLabel("NONE")
		self.T_F3.SetLabel("NONE")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('WALP地理信息系统')
		self.Tip2.SetLabel('什么都没有呢!')
		self.Tip3.SetLabel('什么都没有呢!')
		self.Tip4.SetLabel('什么都没有呢!')

		Function_icon(self, 0, 0, 0, 0, 0, 0, 0, 0)

		self.Refresh()

	def G_7(self, event):
		''' 7号功能分区-物理 '''
		global Main_State, colour_Hover, colour_SideL
		Main_State = 7

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page7.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note7.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G7.SetBackgroundColour(colour_Main)
		self.G7.SetForegroundColour("White")

		self.T_F1.SetLabel("音频分析器")
		self.T_F2.SetLabel("大学评分数据库")
		self.T_F3.SetLabel("二维码")
		self.T_F4.SetLabel("YOLO实时对象检测")

		self.Tip1.SetLabel('对于音频的可视化分析')
		self.Tip2.SetLabel('临时模块-数据库已完成20%')
		self.Tip3.SetLabel('二维码生成系统')
		self.Tip4.SetLabel('基于openCV和YOLOV3数据集的深度神经网络算法')

		Function_icon(self, 0, 0, 0, 0, 0, 0, 0, 0)

		self.Refresh()

	def G_8(self, event):
		''' 8号功能分区-化学 '''
		global Main_State, colour_Hover, colour_SideL
		Main_State = 8

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page8.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note8.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G8.SetBackgroundColour(colour_Main)
		self.G8.SetForegroundColour("White")

		self.T_F1.SetLabel("元素周期表")
		self.T_F2.SetLabel("NONE")
		self.T_F3.SetLabel("NONE")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('经典门捷列夫元素周期表')
		self.Tip2.SetLabel('什么都没有呢!')
		self.Tip3.SetLabel('什么都没有呢!')
		self.Tip4.SetLabel('什么都没有呢!')

		Function_icon(self, 0, 0, 0, 0, 0, 0, 0, 0)

		self.Refresh()

	def G_9(self, event):
		''' 9号功能分区-生物 '''
		global Main_State, colour_Hover, colour_SideL
		Main_State = 9

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page9.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note9.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G9.SetBackgroundColour(colour_Main)
		self.G9.SetForegroundColour("White")

		self.T_F1.SetLabel("基因库")
		self.T_F2.SetLabel("NONE")
		self.T_F3.SetLabel("NONE")
		self.T_F4.SetLabel("NONE")

		self.Tip1.SetLabel('从本地数据库中获取基因数列,然后进行蛋白质转录')
		self.Tip2.SetLabel('什么都没有呢!')
		self.Tip3.SetLabel('什么都没有呢!')
		self.Tip4.SetLabel('什么都没有呢!')

		Function_icon(self, 0, 0, 0, 0, 1, 0, 0, 0)

		self.Refresh()

	def G_10(self, event):
		''' 10号功能分区-通用 '''
		global Main_State, colour_Hover, colour_SideL
		Main_State = 10

		Colour_clean(self)

		start(self)

		colour_cfg = configparser.ConfigParser()
		colour_cfg.read('./DATA/Main/Theme/colourful/Page10.cfg')
		colour_Main = colour_cfg.get('colour', 'colour_Main')
		colour_Bottom = colour_cfg.get('colour', 'colour_Bottom')
		colour_SideL = colour_cfg.get('colour', 'colour_SideL')
		colour_Hover = colour_cfg.get('colour', 'colour_Hover')

		note = open('./DATA/Main/Note/Note10.txt', 'r', encoding='utf-8') # 主界面留言定义
		note = note.readlines()
		roll = random.randint(0, len(note) - 1)
		note = note[roll]
		note = note.replace('\n', '')

		
		Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL)

		self.G10.SetBackgroundColour(colour_Main)
		self.G10.SetForegroundColour("White")

		self.T_F1.SetLabel("随机数生成器")
		self.T_F2.SetLabel("进制转换")
		self.T_F3.SetLabel("值日表")
		self.T_F4.SetLabel("计时器")

		self.Tip1.SetLabel('利用随机数函数生成随机数字')
		self.Tip2.SetLabel('2进制/8进制/10进制/16进制转换')
		self.Tip3.SetLabel('将班级值日表显示在电脑壁纸上!')
		self.Tip4.SetLabel('简单的计时器,真的只是计时')

		Function_icon(self, 0, 0, 0, 0, 0, 0, 1, 0)

		self.Refresh()

###########################################################################
# 文件拖入处理Class
# File Class
###########################################################################

class FileDrop(wx.FileDropTarget):

	def __init__(self, window):

		wx.FileDropTarget.__init__(self)
		self.window = window

	def OnDropFiles(self, x, y, filenames):

		for name in filenames:
			print(name)

			font = int(name.rfind('.')) + 1
			end = int(len(name))
			file_type = str(name)[font: end]

			print('文件类型:' + file_type)

		if len(filenames) > 1:
			print('警告:暂不支持多文件拖放,取最后一个文件')

		File_cfg = configparser.ConfigParser()
		File_cfg.read('./cfg/File.cfg')
		File_cfg.set('File', 'path', name)
		File_cfg.set('File', 'type', str(file_type))
		File_cfg.write(open('./cfg/File.cfg', 'w'))

		wx.CallAfter(wx.MessageBox, '检测到文件:' +  file_type) # 延期呼叫事件--wx自带的一种多线程方法

		##M_File.main() # 如果直接这样打开会阻塞线程,windows资源管理器也会卡住

		return True

###########################################################################
# 窗口拖动处理Class
# Window Move Class
###########################################################################
class WorkerThread(threading.Thread):
    def __init__(self, frame):
        threading.Thread.__init__(self)
        self.frame = frame
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.system_mouse_pos = win32api.GetCursorPos()

    def run(self):
        x = self.system_mouse_pos[0] - self.frame.GetPosition()[0]
        y = self.system_mouse_pos[1] - self.frame.GetPosition()[1]
        while 1:
            self.timeToQuit.wait(0.01)
            if self.timeToQuit.isSet():
                break
            self.system_mouse_pos = win32api.GetCursorPos()
            frame_pos_x = self.system_mouse_pos[0] - x
            frame_pos_y = self.system_mouse_pos[1] - y
            frame_pos = (frame_pos_x, frame_pos_y)
            wx.CallAfter(self.frame.move_start, frame_pos)
        else:
            wx.CallAfter(self.frame.move_stop, self)

###########################################################################
# 主函数
# def main
###########################################################################


def main():
	'''
	主函数
	'''
	app = wx.App(False)  # GUI循环及前置设置
	frame = CalcFrame(None)
	frame.Show(True)

	app.MainLoop()


def Colour_clean(self):
	''' 用于清空全部按钮的颜色设置(GUI) '''
	# 设置按钮背景颜色和字体颜色
	BackGround_Colour = "White"
	Foreground_Colour = "Black"

	self.G1.SetBackgroundColour(BackGround_Colour)
	self.G2.SetBackgroundColour(BackGround_Colour)
	self.G3.SetBackgroundColour(BackGround_Colour)
	self.G4.SetBackgroundColour(BackGround_Colour)
	self.G5.SetBackgroundColour(BackGround_Colour)
	self.G6.SetBackgroundColour(BackGround_Colour)
	self.G7.SetBackgroundColour(BackGround_Colour)
	self.G8.SetBackgroundColour(BackGround_Colour)
	self.G9.SetBackgroundColour(BackGround_Colour)
	self.G10.SetBackgroundColour(BackGround_Colour)

	self.G1.SetForegroundColour(Foreground_Colour)
	self.G2.SetForegroundColour(Foreground_Colour)
	self.G3.SetForegroundColour(Foreground_Colour)
	self.G4.SetForegroundColour(Foreground_Colour)
	self.G5.SetForegroundColour(Foreground_Colour)
	self.G6.SetForegroundColour(Foreground_Colour)
	self.G7.SetForegroundColour(Foreground_Colour)
	self.G8.SetForegroundColour(Foreground_Colour)
	self.G9.SetForegroundColour(Foreground_Colour)
	self.G10.SetForegroundColour(Foreground_Colour)

	BackGround_Colour = None
	Foreground_Colour = None


def Colour_Set(self, note, colour_Main, colour_Bottom, colour_SideL):
	''' 用于设置主界面的颜色(GUI) '''
	self.Note.SetLabel(note)  # 主界面留言设置

	self.version.SetBackgroundColour(colour_Main) # 按钮背景颜色设置
	self.Network.SetBackgroundColour(colour_Main)
	self.Note.SetBackgroundColour(colour_Main)
	self.B_Quit.SetBackgroundColour(colour_Main)
	self.B_Cmd.SetBackgroundColour(colour_Main)
	self.B_Log.SetBackgroundColour(colour_Main)
	self.B_Setting.SetBackgroundColour(colour_Main)
	self.B_About.SetBackgroundColour(colour_Main)
	self.B_Update.SetBackgroundColour(colour_Main)
	self.B_File.SetBackgroundColour(colour_Main)
	self.Weather.SetBackgroundColour(colour_Main)

	# self.SetBackgroundColour('#F9B7B0') # 主界面背景颜色设置
	self.Bottom_Bar1.SetBackgroundColour(colour_Bottom)  # 主界面底部颜色设置
	self.Bottom_Bar2.SetBackgroundColour(colour_Bottom)
	self.Bottom_Bar3.SetBackgroundColour(colour_Bottom)
	self.Bottom_Bar4.SetBackgroundColour(colour_Bottom)
	self.Space1.SetBackgroundColour(colour_Bottom)
	self.Space2.SetBackgroundColour(colour_Bottom)
	self.Space3.SetBackgroundColour(colour_Bottom)

	self.Side1.SetBackgroundColour(colour_SideL)  # 主界面左侧边栏颜色设置
	self.Side2.SetBackgroundColour(colour_SideL)
	self.Side3.SetBackgroundColour(colour_SideL)
	self.Side4.SetBackgroundColour(colour_SideL)


def Log():
	''' Log日志输出 '''
	cfg = configparser.ConfigParser()  # 读取设置文件
	cfg.read('./cfg/main.cfg')
	log_place = cfg.get('main', 'LOG')

	output_dir = log_place  # 定义文件夹位置(不区分大小写)
	log_name = '{}.log'.format(
		time.strftime('%Y-%m-%d-%H-%M'))  # 定义文件后缀名和命名规则
	filename = os.path.join(output_dir, log_name)
	logging.basicConfig(  # LOG设置
		level=logging.DEBUG,  # 输出级别
		filename=filename,  # 文件名
		filemode='w',  # 写入模式,w为重新写入,a为递增写入
		# format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' # 命名规则
	)


def proc_exist(process_name):
	''' 程序运行检查 '''
	is_exist = False
	wmi = win32com.client.GetObject('winmgmts:')
	processCodeCov = wmi.ExecQuery(
		'select * from Win32_Process where name=\"%s\"' % (process_name))
	if len(processCodeCov) > 0:
		is_exist = True
	return is_exist


def start(self):
	'''
	程序初始化界面
	'''
	global setup
	if setup == 1:
		setup = 2
		buer = True
		self.T_F1.Show(buer)
		self.T_F2.Show(buer)
		self.T_F3.Show(buer)
		self.T_F4.Show(buer)

		self.Net1.Show(buer)
		self.Net2.Show(buer)
		self.Net3.Show(buer)
		self.Net4.Show(buer)

		self.File1.Show(buer)
		self.File2.Show(buer)
		self.File3.Show(buer)
		self.File4.Show(buer)

		self.Star1.Show(buer)
		self.Star2.Show(buer)
		self.Star3.Show(buer)
		self.Star4.Show(buer)

		self.Help1.Show(buer)
		self.Help2.Show(buer)
		self.Help3.Show(buer)
		self.Help4.Show(buer)

		self.P_F1.Show(buer)
		self.P_F2.Show(buer)
		self.P_F3.Show(buer)
		self.P_F4.Show(buer)

		self.B_F1.Show(buer)
		self.B_F2.Show(buer)
		self.B_F3.Show(buer)
		self.B_F4.Show(buer)

		self.Tip1.Show(buer)
		self.Tip2.Show(buer)
		self.Tip3.Show(buer)
		self.Tip4.Show(buer)

		self.Side1.Show(buer)
		self.Side2.Show(buer)
		self.Side3.Show(buer)
		self.Side4.Show(buer)

		self.B_Side_Close.Show(buer)
		self.CMD_OUT.Show(buer)
		self.CMD_IN.Show(buer)
		self.Push.Show(buer)

		self.Side_Tip.Show(buer)
		self.info.Show(buer)

		self.Line1.Show(buer)
		self.Line2.Show(buer)
		self.Line3.Show(buer)
		self.Line_Last.Show(False)
		self.Space_left.Show(buer)

		self.Space_topic.Show(False)
		self.Topic.Show(False)
		self.Sub1.Show(False)
		self.Sub2.Show(False)
		self.Fast.Show(False)
		self.Fast_Star1.Show(False)
		self.Fast_Star2.Show(False)
		self.Fast_Star3.Show(False)
		resize(self)
		self.SetBackgroundColour('White')

	elif setup == 0:
		buer = False
		self.T_F1.Show(buer)
		self.T_F2.Show(buer)
		self.T_F3.Show(buer)
		self.T_F4.Show(buer)

		self.Net1.Show(buer)
		self.Net2.Show(buer)
		self.Net3.Show(buer)
		self.Net4.Show(buer)

		self.File1.Show(buer)
		self.File2.Show(buer)
		self.File3.Show(buer)
		self.File4.Show(buer)

		self.Star1.Show(buer)
		self.Star2.Show(buer)
		self.Star3.Show(buer)
		self.Star4.Show(buer)

		self.Help1.Show(buer)
		self.Help2.Show(buer)
		self.Help3.Show(buer)
		self.Help4.Show(buer)

		self.P_F1.Show(buer)
		self.P_F2.Show(buer)
		self.P_F3.Show(buer)
		self.P_F4.Show(buer)

		self.B_F1.Show(buer)
		self.B_F2.Show(buer)
		self.B_F3.Show(buer)
		self.B_F4.Show(buer)

		self.Tip1.Show(buer)
		self.Tip2.Show(buer)
		self.Tip3.Show(buer)
		self.Tip4.Show(buer)

		self.Side1.Show(buer)
		self.Side2.Show(buer)
		self.Side3.Show(buer)
		self.Side4.Show(buer)

		self.B_Side_Close.Show(buer)
		self.CMD_OUT.Show(buer)
		self.CMD_IN.Show(buer)
		self.Push.Show(buer)

		self.Side_Tip.Show(buer)
		self.info.Show(buer)

		self.Line1.Show(buer)
		self.Line2.Show(buer)
		self.Line3.Show(buer)
		self.Line_Last.Show(True)
		self.Space_left.Show(buer)

		setup = 1

	elif setup == 2:
		return


def Home(self):
	'''
	返回初始界面
	'''
	global setup, Main_State, colour_Hover
	colour_Hover = '#A65F00'

	cfg.set('History', 'LAST', FUN_State)
	cfg.set('History', 'MAINSTATE', str(Main_State))
	cfg.set('History', 'COLOR', str(self.Bottom_Bar1.GetBackgroundColour()))
	cfg.write(open('./cfg/main.cfg', 'w'))

	buer = False
	self.T_F1.Show(buer)
	self.T_F2.Show(buer)
	self.T_F3.Show(buer)
	self.T_F4.Show(buer)

	self.Net1.Show(buer)
	self.Net2.Show(buer)
	self.Net3.Show(buer)
	self.Net4.Show(buer)

	self.File1.Show(buer)
	self.File2.Show(buer)
	self.File3.Show(buer)
	self.File4.Show(buer)

	self.Star1.Show(buer)
	self.Star2.Show(buer)
	self.Star3.Show(buer)
	self.Star4.Show(buer)

	self.Help1.Show(buer)
	self.Help2.Show(buer)
	self.Help3.Show(buer)
	self.Help4.Show(buer)

	self.P_F1.Show(buer)
	self.P_F2.Show(buer)
	self.P_F3.Show(buer)
	self.P_F4.Show(buer)

	self.B_F1.Show(buer)
	self.B_F2.Show(buer)
	self.B_F3.Show(buer)
	self.B_F4.Show(buer)

	self.Tip1.Show(buer)
	self.Tip2.Show(buer)
	self.Tip3.Show(buer)
	self.Tip4.Show(buer)

	self.Side1.Show(buer)
	self.Side2.Show(buer)
	self.Side3.Show(buer)
	self.Side4.Show(buer)

	self.B_Side_Close.Show(buer)
	self.CMD_OUT.Show(buer)
	self.CMD_IN.Show(buer)
	self.Push.Show(buer)

	self.Side_Tip.Show(buer)
	self.info.Show(buer)

	self.Line1.Show(buer)
	self.Line2.Show(buer)
	self.Line3.Show(buer)
	self.Line_Last.Show(True)
	self.Space_left.Show(buer)

	self.Space_topic.Show(True)
	self.Topic.Show(True)
	self.Sub1.Show(True)
	self.Sub2.Show(True)
	self.Fast.Show(True)
	self.Fast_Star1.Show(True)
	self.Fast_Star2.Show(True)
	self.Fast_Star3.Show(True)

	botm = wx.Colour(255, 201, 60)
	top = wx.Colour(242, 171, 57)

	self.Bottom_Bar1.SetBackgroundColour(botm)
	self.Bottom_Bar2.SetBackgroundColour(botm)
	self.Bottom_Bar3.SetBackgroundColour(botm)
	self.Bottom_Bar4.SetBackgroundColour(botm)
	self.Space1.SetBackgroundColour(botm)
	self.Space2.SetBackgroundColour(botm)
	self.Space3.SetBackgroundColour(botm)

	self.B_Quit.SetBackgroundColour(top)
	self.B_Cmd.SetBackgroundColour(top)
	self.B_Log.SetBackgroundColour(top)
	self.B_Setting.SetBackgroundColour(top)
	self.B_About.SetBackgroundColour(top)
	self.B_Update.SetBackgroundColour(top)
	self.B_File.SetBackgroundColour(top)

	self.Weather.SetBackgroundColour(top)

	self.Fast.SetLabel(FUN_State)

	Colour_clean(self)

	last = cfg.get('History', 'LAST')

	if last != 'NONE':
		self.Fast.SetLabel(last)
	else:
		self.Fast.SetLabel('NONE')

	if cfg.get('History', 'COLOR') != 'NONE' and tuple(eval(cfg.get('History', 'COLOR'))) != (255, 255, 255, 255):
		self.Fast.SetBackgroundColour(
			wx.Colour(tuple(eval(cfg.get('History', 'COLOR')))))

	Main_State = 0
	setup = 1

	self.Refresh()


def resize(self):
	'''
	通过更改窗口大小触发-->界面刷新
	(这种刷新有别于一般的Refresh,可以让错位的子项复位)
	'''
	self.SetSize(screen_size_x + 1, screen_size_y)
	self.SetSize(screen_size_x, screen_size_y)


def Function_icon(self, Internet1, Internet2, Internet3, Internet4, LocalFile1, LocalFile2, LocalFile3, LocalFile4):
	'''
	功能图标的设置
	'''
	Internet_ON = wx.Image("./pictures/网络-开启20.png",
						   wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	Internet_OFF = wx.Image("./pictures/网络-关闭20.png",
							wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	File_ON = wx.Image("./pictures/文件-开启20.png",
					   wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	File_OFF = wx.Image("./pictures/文件-关闭20.png",
						wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	if Internet1 == 1:
		self.Net1.SetBitmap(Internet_ON)
	else:
		self.Net1.SetBitmap(Internet_OFF)

	if Internet2 == 1:
		self.Net2.SetBitmap(Internet_ON)
	else:
		self.Net2.SetBitmap(Internet_OFF)

	if Internet3 == 1:
		self.Net3.SetBitmap(Internet_ON)
	else:
		self.Net3.SetBitmap(Internet_OFF)

	if Internet4 == 1:
		self.Net4.SetBitmap(Internet_ON)
	else:
		self.Net4.SetBitmap(Internet_OFF)

	if LocalFile1 == 1:
		self.File1.SetBitmap(File_ON)
	else:
		self.File1.SetBitmap(File_OFF)

	if LocalFile2 == 1:
		self.File2.SetBitmap(File_ON)
	else:
		self.File2.SetBitmap(File_OFF)

	if LocalFile3 == 1:
		self.File3.SetBitmap(File_ON)
	else:
		self.File3.SetBitmap(File_OFF)

	if LocalFile4 == 1:
		self.File4.SetBitmap(File_ON)
	else:
		self.File4.SetBitmap(File_OFF)


def Self_CMD(self, info):
	'''
	向程序自带控制台输入信息
	info输入要求:str
	'''
	if self.CMD_OUT.GetValue() == '':
		self.CMD_OUT.SetValue('>>>' + time.strftime('%H:%M:%S') + ':' + info)
	else:
		self.CMD_OUT.SetValue(self.CMD_OUT.GetValue() + '\n' + '>>>' + time.strftime('%H:%M:%S') + ':' + info)


def CMD(self, info):
	'''
	控制台指令处理
	'''
	if info == 'clear' or info == 'clean' or info == 'cls':
		self.CMD_OUT.SetValue('')
	elif info == 'time':
		self.CMD_OUT.SetValue(self.CMD_OUT.GetValue() + '\n' + '>>>Time:' + time.strftime('%H:%M:%S'))
	elif info == 'random' or info == 'stochastic':
		self.CMD_OUT.SetValue(self.CMD_OUT.GetValue() + '\n' + '>>>random:' + str(random.random()))
	elif info == 'close' or info == 'quit' or info == 'kill':
		self.Destroy()
	else:
		self.CMD_OUT.SetValue(self.CMD_OUT.GetValue() + '\n' + '>>>error:' + '未知的指令')

if __name__ == "__main__":
	main()
