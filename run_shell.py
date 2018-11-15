import shlex
import subprocess


def run_cmd(cmd):
    """
    Run a shell command in a subprocess.

    NOTE: `shlex.split(s)` splits the string s using shell-like syntax:
    > shlex.split('ls -lah .')  # ['ls', '-lah', '.']
    The resulting list can be used as an input for `subprocess.call` without the `shell=True` parameter.

    :param cmd: str
    :return: subprocess.CompletedProcess instance
    """
    print('> ' + cmd)

    if cmd.startswith('$('):  # Command substitution
        inner_cmd = shlex.split(cmd.strip('$()'))
        cmd = subprocess.check_output(inner_cmd, encoding='utf-8')  # cmd now is the output of a inner_cmd

    return subprocess.run(shlex.split(cmd))


def run_cmd_pipeline(cmd):
    """
    :param cmd: str
    :return: list of str
    """
    first, *middle, last = (_.strip() for _ in cmd.split('|'))

    prev_process = subprocess.Popen(shlex.split(first), stdout=subprocess.PIPE)
    for cmd in middle:
        prev_process = subprocess.Popen(shlex.split(cmd), stdin=prev_process.stdout, stdout=subprocess.PIPE)

    last_process = subprocess.Popen(shlex.split(last), stdin=prev_process.stdout, stdout=subprocess.PIPE,
                                    encoding='utf-8')

    return [s for s in last_process.communicate()[0].split('\n') if s]


if __name__ == '__main__':
    # run_cmd('$(aws ecr get-login --region eu-west-1 --no-include-email)')

    cmd = 'docker images --all --format "{{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.ID}}" | grep mario'
    print(run_cmd_pipeline(cmd))
