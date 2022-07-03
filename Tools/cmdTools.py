

def run_cmd(cmd_str=''):
    from subprocess import run
    return run(cmd_str, shell=True)