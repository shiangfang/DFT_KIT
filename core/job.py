# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for controling job running process and maintain necessary folders

# next : savepoint? to restart the calculation

import os
import sys
import shutil

class job:
    def __init__(self,subdir=True,job_manager_mode=False,system='DFT simulation',dir_task_prefix='task_',verbosity=True,**parms):
        self.root_dir=os.getcwd()+'/'
        self.subdir=subdir #make subdir structure
        self.all_dir=[]
        self.count=0
        self.main_dir=''
        self.task_prefix=dir_task_prefix
        self.verbose=verbosity
        self.temp_dir=''
        self.scriptmode=False
        self.dft_script_cmds=[]
        
        self.system=system
        self.parms={}
        for ind_key in parms:
            self.parms[ind_key]=parms[ind_key]
        
        if subdir:
            self.create_taskdir()
        else:
            self.main_dir=self.root_dir
            self.all_dir.append(self.main_dir)
        self.common_dir=''
        self.job_mamanger_mode=job_manager_mode
        self.opt_parm={'cpu':1}
            
        #include prefix, filename, etc.
        self.sys_info={'description':'DFT simulation with DFT_KIT',
                       'qes_prefix':'qespre',
                       'qes_fname':'qespresso',
                       'siesta_prefix':'siesta',
                       'wan90_seedname':'wan90'}
        
    def load_opt_parm(self,opt_parm):    
        for ind_key in opt_parm:
            if ind_key=='cpu':
                self.opt_parm['cpu']=int(opt_parm['cpu'])
            else:
                self.opt_parm[ind_key]=opt_parm[ind_key]
    
    def set_job_manager_mode(self,mode):
        self.job_mamanger_mode=mode
    def set_temp_dir(self,dir_name):
        self.temp_dir=self.root_dir+dir_name+'/'
    def set_common_dir(self,full_dir):
        self.common_dir=full_dir
    def copy_from_common(self,fname):
        shutil.copy(self.common_dir+fname,self.main_dir)
    def copy_to_common(self,fname):
        shutil.copy(self.main_dir+fname,self.common_dir)
    def set_sysinfo(self,ind_key,val):
        self.sys_info[ind_key]=val
    def get_sysinfo(self,ind_key):
        return self.sys_info[ind_key]
    def make_fname_sysinfo(self,ind_key):
        return self.sys_info[ind_key]+'_'+str(self.count)
        #create temp/postana dir
    def get_maindir(self):
        return self.main_dir
    
    def set_verbosity(self,verbosity):
        self.verbose=verbosity
    def show_verbose(self,src,message):
        if self.verbose:
            print('DFT_KIT(V):' + src +': ' + message)
        else:
            pass
    def show(self,src,message):
        print('DFT_KIT:' +src +': ' +message)
    def show_error(self,src,message):
        print('DFT_KIT(ERROR):' +src +': ' +message)
    def get_info(self,src,prompt,force_enter):
        tmp_return=''
        if self.scriptmode:
            tmpcmd=self.take_script_cmd()
            self.show(src, prompt +"[S]"+tmpcmd)
            tmp_return = tmpcmd
        else:
            tmp_return = raw_input('DFT_KIT:'+src+': '+prompt+' ')
        while tmp_return =='' and force_enter:
            if self.scriptmode:
                tmpcmd=self.take_script_cmd()
                self.show(src, prompt +"[S]"+tmpcmd)
                tmp_return = tmpcmd
            else:
                tmp_return = raw_input('DFT_KIT:'+src+': '+prompt+' ')
        return tmp_return
            
    def copy_from_task(self,from_task,fname):
        dir_from=self.all_dir[from_task]
        dir_to=self.main_dir
        shutil.copy(dir_from+fname, dir_to)
    
    def create_taskdir(self):
        if not self.subdir:
            self.show_error('DFT_job', 'subdir not properly set')
            return 0
        dir_tmp=self.root_dir+self.get_task_dirname(self.count)+'/'
        self.all_dir.append(dir_tmp)
        os.mkdir(dir_tmp)
        os.chdir(dir_tmp)
        self.main_dir=dir_tmp
        self.count=self.count+1
    def get_task_dirname(self,task_):
        return self.task_prefix+str(task_)
        
    def set_parms(self,ind_key,parm_val):
        self.parms[ind_key]=parm_val
    def get_parms(self,ind_key):
        return self.parms[ind_key]
    def remove_parms(self,ind_key):
        del self.parms[ind_key]
    def next_task(self,make_new_dir):
        if make_new_dir and self.subdir:
            self.show('job', 'create new task and its directory')
            self.create_taskdir()
        else:
            self.show('job', 'create new task')
            self.count=self.count+1
            self.all_dir.append(self.main_dir)
    def make_fname(self,prefix):
        return prefix+'_'+str(self.count)
    def load_script(self,scriptfile):
        with open(scriptfile) as fp:
            for line in fp:
                if line[-1]=='\n':
                    line=line[:-1]
                    self.dft_script_cmds.append(line)
        if len(self.dft_script_cmds)>0:
            self.scriptmode=True
            
    def take_script_cmd(self):
        if not self.scriptmode:
            self.show_error('DFT_job','Not in script mode')
            return ''
        if len(self.dft_script_cmds)==1:
            self.scriptmode=False
        if len(self.dft_script_cmds)>=1:
            cmd=self.dft_script_cmds.pop(0)
            return cmd
        else:
            self.show_error('DFT_job','Not consistent in script mode')
            self.scriptmode=False
            return ''
