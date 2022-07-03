

def run_cmd(cmd_str='', echo_print=1):
    from subprocess import run
    # if echo_print == 1:
    #     print('\n执行cmd指令="{}"'.format(cmd_str))
    return run(cmd_str, shell=True)