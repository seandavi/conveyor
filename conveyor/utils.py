import subprocess
import shlex

def safe_run(cmd,shell=False):
    res = None
    if(isinstance(cmd,list)):
        res = subprocess.call(cmd)
    else:
        if(shell):
            res = subprocess.call(cmd,shell=True)
        else:
            res = subprocess.call(shlex.split(cmd))
    return(res)
