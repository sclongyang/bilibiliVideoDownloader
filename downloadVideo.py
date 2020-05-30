# import os
# import time
import datetime
import sys
import you_get
import os
import subprocess
from you_get import common


def download(url, path):
    sys.argv = ['you-get', "--playlist", url, "-o", path]
    you_get.main()

def deleteFilesByType(dir, typeStr):#如果需要删除更多目录下的文件，可以传两个元组进来，一个元组存放路径(字符串类型)，一个元组存放指定删除的文件格式(字符串类型)。
  for root, dirs, files in os.walk(dir):#os.walk()返回元组，包含三个元素:每次遍历的路径名、路径下子目录列表、目录下文件列表
    for name in files:
      if name.endswith(typeStr): #指定要删除的文件格式，这里是xml，可以换成其他格式
        os.remove(os.path.join(root, name))
        

def execCmd(cmd):  
    r = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    text = r.stdout.read().decode("utf-8")
    return text  

def main():
    if __name__ == '__main__':            
        curFilePath = os.path.realpath(__file__)
        workDir = os.path.dirname(curFilePath)
        startFrom = ""
        if len(sys.argv) > 1:
            startFrom = sys.argv[1]        
            
        f=open(workDir + "\\video_url.txt",'r')
        s=f.readlines() 
        rootDir = workDir +"\\download_fermi"
        if not os.path.exists(rootDir):
            os.mkdir(rootDir)

        dirs=[]
        for url in s: 
            url = url.strip()

            info = execCmd("you-get -i " + url)
            titleStr = "title:"
            idx1 = info.find(titleStr)
            idx2 = info.find("streams:")            
            titleName = info[idx1 + len(titleStr) : idx2].strip()          
            downloadDir = rootDir +"\\"+ titleName
            if downloadDir in dirs:
                print("已跳过重复的url:"+downloadDir)
                continue
            else:
                dirs.append(downloadDir)            

            if startFrom != "":
                if not titleName.startswith(startFrom):
                    print("title与startFrom参数不匹配, 跳过:" + titleName)
                    continue
            startFrom=""            
            if not os.path.exists(downloadDir):
                os.mkdir(downloadDir)

            # 会自动跳过已下载的文件
            download(url, downloadDir)

            # 删除多余的xml文件
            deleteFilesByType(downloadDir, ".xml")

            # # 修改目录名
            # listDir = os.listdir(downloadDir)     
            # firstFileName = listDir[0]    
            # newDirName = rootDir + "\\" + firstFileName + "_"+ dirName
            # os.rename(downloadDir, newDirName)   
            
main()
