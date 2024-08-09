import os
import subprocess
import sys
import pkg_resources
import hashlib

Import("env")

missing = True

for pkg in pkg_resources.working_set:
    if pkg.key == "stm8dce" and pkg.version >= "1.1.1":
        missing = False
        break

if missing:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "stm8dce>=1.1.1"]
        )
    except:
        sys.stderr.write(
            "stm8dce tool not found, install it via https://github.com/CTXz/STM8-DCE"
        )
        env.Exit(-1)


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def optimize_asm(source, target, env):

    temp_out_dir = os.path.join(env.subst("$BUILD_DIR"), "stm8dce_output")
    os.makedirs(temp_out_dir, exist_ok=True)

    asm_path = ""
    stm8dce_fold_asm = []
    asm_hash_old = []

    for x in source:

        tst_asm_pth = os.path.join(
            temp_out_dir, os.path.splitext(
                os.path.basename(str(x)))[0] + ".asm"
        )

        if os.path.isfile(tst_asm_pth):
            asm_hash_old.append(sha256sum(tst_asm_pth))
        else:
            asm_hash_old.append("")

        stm8dce_fold_asm.append(tst_asm_pth)

        tst_asm_pth = os.path.splitext(str(x))[0] + ".asm"
        if os.path.isfile(tst_asm_pth):
            asm_path += ' "' + tst_asm_pth + '"'

    env.Execute(
        env.VerboseAction(
            "stm8dce "
            + " -o "
            + '"'
            + temp_out_dir
            + '" '
            + env.GetProjectOption("stm8dce_flags", default="")
            + (" -v" if int(ARGUMENTS.get("PIOVERBOSE", 0)) else "")
            + ' "'
            + '" "'.join(map(str, source))
            + '"'
            + asm_path,
            "STM8DCE CODE OPTIMIZATION",
        )
    )

    for x, asm_pt, hs_old in zip(source, stm8dce_fold_asm, asm_hash_old):

        if os.path.isfile(asm_pt):
            if hs_old:
                if sha256sum(asm_pt) == hs_old:
                    continue

            env.Execute(
                env.VerboseAction(
                    "$AS -plosg -ff -o " + '"' +
                    str(x) + '" "' + asm_pt + '"',
                    "COMPILING " + str(x),
                )
            )


env.AddPreAction(
    "$BUILD_DIR/${PROGNAME}.elf", env.VerboseAction(
        optimize_asm, "EXTRA SCRIPT")
)
