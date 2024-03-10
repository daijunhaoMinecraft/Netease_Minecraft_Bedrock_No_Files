# -*- coding:utf-8 -*-
import wx
import winreg
import datetime
import os
import concurrent.futures
import shutil

pathx = os.path.dirname(os.path.abspath(__file__))

def copy_and_replace(source_folder, destination_folder):
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        def copy_files(src, dst):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    if not os.path.exists(d):
                        os.makedirs(d)
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        executor.submit(copy_files, s, d)  # 在创建新的线程池中执行复制文件操作
                else:
                    shutil.copy2(s, d)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(copy_files, source_folder, destination_folder)

        executor.shutdown()  # 清理资源
        return f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}修改成功!\n"
    except Exception:
        return f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}修改失败!\n"

def delete_folder_content(folder_path):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(delete_folder_content, file_path)
                os.rmdir(file_path)
        return f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}删除目录成功!\n"
    except Exception:
        return f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}删除目录失败!\n"
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='网易我的世界基岩版去除网易无用文件--节省空间占用 By:daijunhao 仅供学习交流,严禁用于商业用途,请于24小时内删除', size=(1000, 700),name='frame',style=541072384)
        self.启动窗口 = wx.Panel(self)
        self.Centre()
        self.Bedrock_Netease_Path = wx.TextCtrl(self.启动窗口,size=(700, 22),pos=(226, 46),value='',name='text',style=16)
        self.Bedrock_4399_Path = wx.TextCtrl(self.启动窗口,size=(700, 22),pos=(226, 91),value='',name='text',style=16)
        self.标签3 = wx.StaticText(self.启动窗口,size=(80, 24),pos=(24, 15),label='请选择版本',name='staticText',style=0)
        标签3_字体 = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.标签3.SetFont(标签3_字体)
        self.Bedrock_Netease = wx.RadioButton(self.启动窗口,size=(190, 24),pos=(24, 44),name='radioButton',label='当前网易我的世界基岩版路径:')
        self.Bedrock_4399 = wx.RadioButton(self.启动窗口,size=(192, 24),pos=(24, 89),name='radioButton',label='当前4399版我的世界基岩版路径:')
        self.No_netease_files = wx.CheckBox(self.启动窗口,size=(473, 24),pos=(26, 153),name='check',label='去除网易我的世界无用文件',style=16384)
        self.Debug = wx.TextCtrl(self.启动窗口,size=(927, 315),pos=(26, 254),value='',name='text',style=1073741872)
        self.我的世界_to_Minecraft = wx.CheckBox(self.启动窗口,size=(473, 24),pos=(26, 187),name='check',label='将"我的世界"标题修改成"Minecraft"标题',style=16384)
        self.标签4 = wx.StaticText(self.启动窗口,size=(80, 24),pos=(26, 223),label='Debug日志:',name='staticText',style=0)
        self.start_yes = wx.Button(self.启动窗口,size=(138, 52),pos=(26, 587),label='开始执行',name='button')
        start_yes_字体 = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.start_yes.SetFont(start_yes_字体)
        self.start_yes.Bind(wx.EVT_BUTTON,self.start_yes_按钮被单击)
        self.clean_debug = wx.Button(self.启动窗口, size=(80, 32), pos=(873, 208), label='清空日志', name='button')
        clean_debug_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.clean_debug.SetFont(clean_debug_字体)
        self.clean_debug.Bind(wx.EVT_BUTTON, self.clean_debug_按钮被单击)
        try:
            def windowsmc_Netease_path():
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
                path = winreg.QueryValueEx(key, "MinecraftBENeteasePath")[0]
                return path
            self.Bedrock_Netease_Path.SetLabel(f"{windowsmc_Netease_path()}")
        except FileNotFoundError as Error:
            self.Bedrock_Netease.Disable()
            self.Bedrock_Netease_Path.SetLabel("当前不可用,请检查你是否安装该版本")
        try:
            def windowsmc_4399_path():
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\PC4399_MCLauncher')
                path = winreg.QueryValueEx(key, "MinecraftBENeteasePath")[0]
                return path
            self.Bedrock_4399_Path.SetLabel(f"{windowsmc_4399_path()}")
        except FileNotFoundError as Error:
            self.Bedrock_4399.Disable()
            self.Bedrock_4399_Path.SetLabel("当前不可用,请检查你是否安装该版本")



    def start_yes_按钮被单击(self,event):
        if self.Bedrock_Netease.GetValue() == True:
            windowsmc_path = self.Bedrock_Netease_Path.GetValue()
        elif self.Bedrock_4399_Path.GetValue() == True:
            windowsmc_path = self.Bedrock_4399_Path.GetValue()
        elif self.Bedrock_Netease.GetValue() == False and self.Bedrock_4399.GetValue() == False:
            select_version_Error = wx.MessageDialog(None, caption="Error",message="请选择版本",style=wx.OK | wx.ICON_ERROR)
            if select_version_Error.ShowModal() == wx.ID_OK:
                pass
        if self.No_netease_files.GetValue() == True:
            self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}--------去除网易我的世界无用文件--------\n")
            self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}当前正在执行命令:去除网易我的世界多余文件\n")
            if os.path.exists(f"{windowsmc_path}\\windowsmc"):
                if os.path.exists(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\revise_ok.txt"):
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}出现错误:你已经执行过了\n")
                else:
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\textures\\ui\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\textures\\ui"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\textures\\sfxs\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\textures\\sfxs"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\textures\\models\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\textures\\models"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\models\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\models"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\shaders\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\shaders"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\render_controllers\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\render_controllers"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\particles\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\particles"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\materials\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\materials"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\graphics_settings\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\graphics_settings"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\animation_controllers\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\animation_controllers"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\animations\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\animations"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除文件夹:{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\effects\\*.*\n")
                    self.Debug.AppendText(delete_folder_content(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\effects"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在修复地图文件\n")
                    self.Debug.AppendText(copy_and_replace(f"{pathx}\\vanilla_netease_fix_map",f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease"))
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在删除部分无效文件\n")
                    debug_del = os.popen(f"del /f /s /q {windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\language_names.json").read()
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}{debug_del}\n")
                    debug_del = os.popen(f"del /f /s /q {windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\languages.json").read()
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}{debug_del}\n")
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}完成,正在修改contents.json文件\n")
                    with open(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\contents.json",mode="w",encoding="utf-8") as f:
                        f.write("")
                        f.close()
                    with open(f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla_netease\\revise_ok.txt",mode="w",encoding="utf-8") as f:
                        f.write("")
                        f.close()
                    self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}Done!\n")
            else:
                self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}出现错误:未检测到网易我的世界基岩版文件(windowsmc文件)请检查你是否安装了网易我的世界基岩版\n")
        if self.我的世界_to_Minecraft.GetValue() == True:
            self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}--------网易我的世界标题修改--------\n")
            self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}当前正在执行命令:去除网易我的世界多余文件\n")
            if os.path.exists(f"{windowsmc_path}\\windowsmc"):
                self.Debug.AppendText(copy_and_replace(f"{pathx}\\vanilla_Minecraft_icon", f"{windowsmc_path}\\windowsmc\\data\\resource_packs\\vanilla"))
                self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}Done!\n")
            else:
                self.Debug.AppendText(f"{datetime.datetime.now().strftime('[date:%Y-%m-%d time:%H:%M:%S]')}出现错误:未检测到网易我的世界基岩版文件(windowsmc文件)请检查你是否安装了网易我的世界基岩版\n")
        if self.No_netease_files.GetValue() == False and self.我的世界_to_Minecraft.GetValue() == False:
            select_Error = wx.MessageDialog(None, caption="Error",message="请选择一个项",style=wx.OK | wx.ICON_ERROR)
            if select_Error.ShowModal() == wx.ID_OK:
                pass

    def clean_debug_按钮被单击(self,event):
        clean_debug_warm = wx.MessageDialog(None, caption="警告", message="确定要清空日志?", style=wx.YES_NO | wx.ICON_WARNING)
        if clean_debug_warm.ShowModal() == wx.ID_YES:
            self.Debug.SetLabel("")
            clean_debug_info = wx.MessageDialog(None, caption="info", message="日志已清空完毕",style=wx.OK | wx.ICON_INFORMATION)
            if clean_debug_info.ShowModal() == wx.ID_OK:
                pass










class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()