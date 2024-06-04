import os
import shutil
import sys
Import("env")

# Sanity check that tool was installed
if shutil.which("stm8dce") is None:
    sys.stderr.write("stm8dce tool not found, install it via https://github.com/CTXz/STM8-DCE")
    env.Exit(-1)

def optimize_asm(source, target, env):
    rel_files: list[str] = [str(x) for x in source]
    #print("Optimize asm called for source: " + str(rel_files) + " target: " + str(target))
    # try to infer .asm filename
    asm_files = [x.replace(".rel", ".asm") for x in rel_files]        
    # construct stm8dce command
    temp_out_dir = os.path.join(env.subst("$BUILD_DIR"), "optim_output")
    if not os.path.isdir(temp_out_dir):
        os.mkdir(temp_out_dir)
    print("Optimizing output.")
    env.Execute(
        " ".join([
            "stm8dce",
            "-o",
            # could also add more --opt-irq, -e, -xf, -xc options here
            "\"" + temp_out_dir + "\""
            ] + ["\"" + x + "\"" for x in asm_files]
        )
    )
    # move back generated files
    for root, dirs, files in os.walk(temp_out_dir):
        for file in files:
            # try to find original path in asm_files
            orig_path = list(filter(lambda path: path.endswith(file), asm_files))
            if len(orig_path) == 1:
                #print("Moving " + os.path.join(temp_out_dir, file) + " to " + orig_path[0])
                shutil.move(os.path.join(temp_out_dir, file), orig_path[0])

    # We have to regenerate the .rel, .lst and .sym files by assembling them from the new optimized .asm files
    for asm_file, rel_file in zip(asm_files, rel_files):
        env.Execute(" ".join([
            "$AS", 
            "-plosg", "-ff", "\"" + rel_file + "\"",
            "\"" + asm_file + "\""]))

    # remove temp dir again
    os.rmdir(temp_out_dir)

env.AddPreAction("$BUILD_DIR/${PROGNAME}.elf", optimize_asm)