import os
import shutil
import sys
import subprocess
import pkg_resources
Import("env")

missing=True

for pkg in pkg_resources.working_set:
    if pkg.key=="stm8dce" and pkg.version>="1.1.1":
        missing=False
        
if missing:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade","pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "stm8dce>=1.1.1"])
    except:
         sys.stderr.write("stm8dce tool not found, install it via https://github.com/CTXz/STM8-DCE")
         env.Exit(-1)



def optimize_asm(source, target, env):
    
    temp_out_dir = os.path.join(env.subst("$BUILD_DIR"), "optim_output")
    if not os.path.isdir(temp_out_dir):
        os.mkdir(temp_out_dir)

    stm8dce_flags=   env.GetProjectOption("stm8dce_flags", default="") 
    
    asm_path=""

    for x in source:
      tst_asm_pth= os.path.splitext(str(x))[0]+".asm"  
      if  os.path.isfile(tst_asm_pth):
        asm_path += ' "' + tst_asm_pth +'"'

    env.Execute(env.VerboseAction("stm8dce "  + 
    stm8dce_flags  +
    (" -v " if int(ARGUMENTS.get("PIOVERBOSE", 0)) and  (" "+stm8dce_flags+" ").find(" -v ")<0  else "") +
    " -o " + 
    '"' + temp_out_dir + 
    '" "' +
    '" "'.join(map(str,source))+ '"' + asm_path, "STM8DCE CODE OPTIMIZATION"))
  
    for x in source:
        tmp_path= os.path.join(temp_out_dir,os.path.splitext(os.path.basename(str(x)))[0]+".asm") 
        if  os.path.isfile(tmp_path):
            env.Execute(env.VerboseAction("$AS -plosg -ff -o " + '"' +str(x) +'" "' +tmp_path+'"',"COMPILING "+str(x) ))
            os.remove(tmp_path)
            
    if not os.listdir(temp_out_dir):
        os.rmdir(temp_out_dir)

env.AddPreAction("$BUILD_DIR/${PROGNAME}.elf", env.VerboseAction(optimize_asm,"EXTRA SCRIPT"))
