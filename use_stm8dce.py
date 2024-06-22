import os
import shutil
import sys
Import("env")

# Sanity check that tool was installed
if shutil.which("stm8dce") is None:
    sys.stderr.write("stm8dce tool not found, install it via https://github.com/CTXz/STM8-DCE")
    env.Exit(-1)
    
def optimize_asm(source, target, env):
    
    temp_out_dir = os.path.join(env.subst("$BUILD_DIR"), "optim_output")
    if not os.path.isdir(temp_out_dir):
        os.mkdir(temp_out_dir)

    env.Execute("stm8dce "  + 
    env.GetProjectOption("stm8dce_flags", default="")   +
    (" -v " if int(ARGUMENTS.get("PIOVERBOSE", 0)) else "") +
    " -o " + 
    '"' + temp_out_dir +  
    '" "'+
    '" "'.join( [os.path.splitext(str(x))[0]+".asm"   for x in source])+ '"' )    
  
    for x in source:
        tmp_path= os.path.join(temp_out_dir,os.path.splitext(os.path.basename(str(x)))[0]+".asm") 
        env.Execute("$AS -plosg -ff -o " + '"' +str(x) +'" "' +tmp_path+'"' )
        os.remove(tmp_path)

    os.rmdir(temp_out_dir)

env.AddPreAction("$BUILD_DIR/${PROGNAME}.elf", optimize_asm)
