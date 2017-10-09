import yaml
import sys
import subprocess
from fs.osfs import OSFS
from fs.copy import copy_file, copy_fs
from fs import path
import requests


def copy_mac(source, target, mac_name):
    with OSFS(source), OSFS(target) as s, t:
        copy_file(s, mac_name, t, mac_name)


def copy_dir(source, target):
    filters = ['*.mac', '*.sh', '*.C', '*.pat', '*.db', '*']
    with OSFS(source) as s:
        with OSFS(target) as t:
            for f in s.filterdir('.', files=filters, exclude_dirs=['*']):
                copy_file(s, f.name, t, f.name)


def copy_group(source, target, group_name):
    with OSFS(source) as s:
        with s.opendir(group_name) as sd:
            with OSFS(target) as t:
                copy_dir(sd.getsyspath('.'), t.getsyspath('.'))


def make_run_sh(target, file_name, main_mac, analysis_c):
    with OSFS(target) as t:
        with t.open(file_name, 'w') as fout:
            c = ("#!/bin/bash\n"
                 + "#SBATCH -o %J.out\n"
                 + "#SBATCH -e %J.err\n"
                 + "source ~/.zshrc\n"
                 + "date\n"
                 + "Gate {mac}\n".format(mac=main_mac)
                 + "root -q -b {cfile}\n".format(cfile=analysis_c)
                 #  + "echo datadata > result.txt\n"
                 #  + "sleep 600\n"
                 #  + "echo datadata > result.txt\n"
                 + "date\n")
            print(c, file=fout)


def make_post_sh(target, file_name):
    with OSFS(target) as t:
        with t.open(file_name, 'w') as fout:
            c = ("#!/bin/bash\n"
                 + "#SBATCH -o %j.out\n"
                 + "#SBATCH -e %j.err\n"
                 + "source ~/.zshrc\n"
                 + "date\n"
                 + "pygate merge\n"
                 + "pygate clear_subdirs\n"
                 + "date\n")
            print(c, file=fout)


def make_sub(target, sub_id):
    with OSFS(target) as t:
        sub = t.makedir('sub{:d}'.format(sub_id), recreate=True)
    copy_dir(target, sub.getsyspath('.'))


def make_subs(target, nb_split):
    for i in range(nb_split):
        make_sub(target, i)


def merge(targe, merge_file_name):
    with OSFS(targe) as t:
        with t.open(merge_file_name, 'w') as fout:
            for f in t.walk.files(filter=[merge_file_name]):
                if path.issamedir('/', f):
                    continue
                with t.open(f) as fin_tmp:
                    print(fin_tmp.read(), end='', file=fout)


def submit_service_print(run_infos, post_infos):
    for t in run_infos:
        print('RUN: ', 'DIR: ', t[0], 'FILE: ', t[1])
    print('POST: ', 'DIR: ', post_infos[0], 'FILE: ', post_infos[1])


def submit_service_direct(run_infos, post_infos):
    for t in run_infos:
        cmd = 'cd {dir} && sbatch {file}'.format(dir=t[0], file=t[1])
        with subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE) as p:
            print(p.stdout.read().decode())


def submit_service_hqlf(run_infos, post_infos):    
    from dxpy.task.representation import creators
    from dxpy.task import interface
    tasks = []
    for i, t in enumerate(run_infos):

        desc = '<PYGATE {0}>.RUN #{1}'.format(post_infos[0], i)
        tasks.append(creators.task_slurm(file=t[1], workdir=t[0], desc=desc))
    tasks.append(creators.task_slurm(file=post_infos[1],
                                     workdir=post_infos[0],
                                     desc='<PYGATE {0}>.POST'.format(post_infos[0])))
    depens = [None] * (len(tasks) - 1)
    depens.append(list(range(len(tasks) - 1)))
    g = creators.task_graph(tasks, depens)
    ids = interface.create_graph(g)
    print('Submitted to HQLF.Task with tids:', ids)


def submit(target, run_sh, post_sh, submit_service):
    """
    Inputs:
    - target: path of work directory,        
    - url: url of task manager,
    - submit_service: a Slurm submit service with args: workdir, file_name
    """
    with OSFS(target) as t:
        run_infos = []
        for d in t.walk.dirs(filter=['sub*']):
            run_infos.append((t.getsyspath(d), run_sh))
        post_infos = (t.getsyspath('.'), post_sh)
        submit_service(run_infos, post_infos)


def clear_all(target, config, no_action=False):
    with OSFS(target) as t:
        for f in t.filterdir(path='.', exclude_files=[config]):
            if f.name.endswith('.yml'):
                continue
            if no_action:
                print('TO DELTE: {0}/{1}.'.format(t.getsyspath('.'), f.name))
            else:
                if f.is_dir:
                    t.removetree(f.name)
                else:
                    t.remove(f.name)


def clear_subdirs(target, no_action=False):
    with OSFS(target) as t:
        for d in t.filterdir(path='.', exclude_files=['*'], dirs=['sub*']):
            if no_action:
                print('TO DELTE: {0}/{1}.'.format(t.getsyspath('.'), d.name))
            else:
                t.removetree(d.name)


def run(target, mac_file, stdout=None, stderr=None):
    if stdout is None:
        stdouts = sys.stdout
    else:
        stdouts = open(stdout, 'w')
    if stderr is None:
        stderrs = sys.stderr
    else:
        stderrs = open(stderr, 'w')
    with subprocess.Popen(['Gate', mac_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        stdouts.write(p.stdout.read().decode())
        stderrs.write(p.stderr.read().decode())
