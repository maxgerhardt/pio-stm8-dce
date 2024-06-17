import os
import shutil
import sys
Import("env")

# Sanity check that tool was installed
if shutil.which("stm8dce") is None:
    sys.stderr.write("stm8dce tool not found, install it via https://github.com/CTXz/STM8-DCE")
    env.Exit(-1)

env.Append(CFLAGS=["-S"])#тут короче хрень, платформио убирает этот флаг при компиляции то есть гъде-то ставит гъде-то нет короч подремонтируйте

def optimize_asm(source, target, env):

    all_path = ""

    temp_out_dir = os.path.join(env.subst("$BUILD_DIR"), "optim_output")
    if not os.path.isdir(temp_out_dir):
        os.mkdir(temp_out_dir)


    for x in source:
        tmp_path=os.path.splitext(str(x))[0]+".asm" 
        all_path+= " " + tmp_path
        if not os.path.isfile(tmp_path): 
            os.rename(str(x),tmp_path)
    
    env.Execute("stm8dce -o "+ temp_out_dir + all_path)    
  
    for x in source:
        tmp_path=os.path.join(temp_out_dir,os.path.splitext(os.path.basename(str(x)))[0]+".asm")
        env.Execute("$AS -plosg -ff -o " + str(x) + " " +tmp_path )
        os.remove(tmp_path)

    os.rmdir(temp_out_dir)


env.AddPreAction("$BUILD_DIR/${PROGNAME}.elf", optimize_asm)
