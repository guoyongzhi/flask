import os
import json
import time


class simulate_TS(object):
    def __init__(self, folderPath):
        self.folderPath = folderPath
    
    def get_folder(self):
        dirList = []
        fileList = []
        files = os.listdir(self.folderPath)  # 文件夹下所有目录的列表
        print('files:', files)
        for f in files:
            if os.path.isdir(self.folderPath + '/' + f):  # 这里是绝对路径，该句判断目录是否是文件夹
                dirList.append(f)
            elif os.path.isfile(self.folderPath + '/' + f):  # 这里是绝对路径，该句判断目录是否是文件
                fileList.append(f)
        print("文件夹有：", dirList)
        print("文件有：", fileList)
        return dirList
    
    def get_new_list(self):
        dirList = self.get_folder()
        newdir_list = []
        for dir in dirList:
            newdir = os.path.join(self.folderPath, dir)
            newdir_list.append(newdir)
        return newdir_list
        
    def read_json(self):
        newdir_list = self.get_new_list()
        p_list = ['失联.txt', '未归.txt', '晚归.txt', '正常.txt']
        for n in newdir_list:
            with open(os.path.join(n, 'TParam.json'), 'r') as f:
                name_info = f.readlines()
                TSdict = json.loads(name_info[0])
                f.close()
            for p in p_list:
                with open(os.path.join(n, p), 'r') as lf:
                    Card_list = lf.readlines()[0].split(',')
                    lf.close()
                TSdict['CardNums'] = Card_list
                if p[:2] == '未归':
                    TSdict['SwipingModel'] = 4
                else:
                    TSdict['SwipingModel'] = 3
                all_dit = os.path.join(n, p[:2])
                if os.path.exists(all_dit) and os.path.isdir(all_dit):
                    pass
                else:
                    os.mkdir(all_dit)
                with open(os.path.join(all_dit, 'TParam.json'), 'w', encoding='cp936') as wf:
                    # json.dump(TSdict, wf, indent=2, sort_keys=True, ensure_ascii=False)
                    wf.write(json.dumps(TSdict))
                    wf.close()
                    print(os.path.join(all_dit, 'TParam.json'), '完成')
                # with open(os.path.join(all_dit, 'TParam.json'), 'r', ) as ff:
                #     TTSdict = json.loads(ff.readlines()[0])
                #     wf.close()
        return True

    
if __name__ == '__main__':
    st = simulate_TS(r'I:\test-work\2.0优化\ts')
    st.read_json()
