import yaml
import sys
import subprocess
import warnings
from dxpy.filesystem import Path
from fs.osfs import OSFS
from fs import copy as fc
from fs import path as fp
import requests
from . import methods
from .shell import ShellScript
from .template.service import MacMaker


class EnsureFS:
    def __init__(self, fs):
        if isinstance(fs, str):
            self.fs = OSFS(fs)
            self.need_close = True
        else:
            self.fs = fs
            self.need_close = False

    def __enter__(self):
        return self.fs

    def __exit__(self, type, value, trackback):
        if self.need_close:
            self.fs.close()


def copy_file(source, target, name):
    """
    Inputs:
        source: directory, str or fs.baseFS
        target: directory, str or fs.baseFS
        name: filename, str
    Raises:
        None
    Returns:
        None
    """
    with EnsureFS(source) as fss, EnsureFS(target) as fst:
        fc.copy_file(fss, name, fst, name)


def copy_dir(source, target, filters=None):
    with EnsureFS(source) as fss, EnsureFS(target) as fst:
        filters = filters or ['*']
        (methods.files(fss, filters)
            .subscribe(lambda f: copy_file(fss, fst, f)))


def copy_group(source, target, group_name):
    with EnsureFS(source) as fss, EnsureFS(target) as fst:
        with fss.opendir(group_name) as sd:
            copy_dir(sd, fst)


class ConfigMaker:
    DEFAULT_CONFIGS = """#configs file of pygate
templates_directory: '/hqlf/hongxwing/macs_template/SPECT'
target: '.'
nb_split: 10
shell:
  type: zsh
  run: run.sh
  post: post.sh
clear:
  keep: [pygate.yml, experiment.yml]
submit: hqlf
merge: 
  method: hadd
  filenames: [result.root]
tasks:
  - name: Gate
    group: run
    payloads:
      filename: some.mac
  - name: merge
    group: post
    payloads:
      
  - name: root
    group: post
    payloads:
      filename: some_analysis.C
template:
    files: ['experiment.yml']
verbose: 0
dryrun: false

"""

    DEFAULT_CONFIG_FILENAME = 'pygate.yml'

    @classmethod
    def make(cls, target, config_filename=None, fs=None):
        import pygate
        # with open(Path(pygate.__file__).father)
        if fs is None:
            fs = OSFS
        config_filename = config_filename or cls.DEFAULT_CONFIG_FILENAME
        with fs(target) as t:
            with t.open(config_filename, 'w') as fout:
                print(cls.DEFAULT_CONFIGS, file=fout)
        MacMaker.make_yml('experiment')


class Initializer:
    @classmethod
    def init(cls, c):
        pass

    @classmethod
    def templates(cls, c):
        copy_dir(c['templates_directory'], c['target'])

    @classmethod
    def shell(cls, c):
        ShellMaker.run(c['shell']['run'])

    @classmethod
    def mac(cls, c):
        MacMaker.make_mac(c['template']['files'])


class ShellMaker:
    @classmethod
    def run(target, c):
        with OSFS(c['target']) as t:
            with t.open(c['shell']['run'], 'w') as fout:
                tasks = [{'name': t['name'], 'payloads': t['payloads']}
                         for t in c['tasks'] if t['group'] == 'run']
                s = ShellScript(fout, tasks, c['shell']['type'])
                s.dump()

    @classmethod
    def post(target, c):
        with OSFS(c['target']) as t:
            with t.open(c['shell']['post'], 'w') as fout:
                tasks = [{'name': t['name'], 'payloads': t['payloads']}
                         for t in c['tasks'] if t['group'] == 'post']
                s = ShellScript(fout, tasks, c['shell']['type'])
                s.dump()


class SubDirectoryMaker:
    @classmethod
    def make_sub(cls, target, sdid):
        with OSFS(target) as t:
            sub = t.makedir('sub.{:d}'.format(sdid), recreate=True)
            copy_dir(target, sub)

    @classmethod
    def make_subs(cls, c):
        for i in range(c['nb_split']):
            cls.make_sub(c['target'], i)


class Merger:
    @classmethod
    def hadd(cls, fs, target, filenames, dryrun=False):
        path_target = fs.getsyspath(target)
        path_filenames = [fs.getsyspath(f) for f in filenames if fs.exists(f)]
        call_args = ['hadd', path_target] + path_filenames
        if dryrun:
            print(' '.join(call_args))
        else:
            with subprocess.Popen(call_args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as p:
                sys.stdout.write(p.stdout.read().decode())
                sys.stderr.write(p.stderr.read().decode())

    @classmethod
    def direct(cls, fs, target, filenames):
        with fs.open(targe, 'w') as fout:
            for f in filenames:
                with fs.open(f) as fin:
                    print(fin.read(), end='', file=fout)

    @classmethod
    def merge(cls, c):
        method = (c.get('merge') or {}).get('method') or 'DIRECT'
        files_to_merge = ((c.get('merge') or {}).get('filenames') or [])
        with OSFS(c['target']) as fs:
            for mfn in files_to_merge:
                filenames = []
                (methods.Mapper(fs).files(mfn)
                    .subscribe(filenames.append))
                if method.upper() == 'HADD':
                    cls.hadd(fs, mfn, filenames, c.get('dryrun'))
                elif method.upper() == 'DIRECT':
                    cls.direct(fs, mfn, filenames)


class Submitter:
    @classmethod
    def service(cls, name):
        name = name.upper()
        SERVICE = {
            'PRINT': cls.sprint,
            'DIRECT': cls.direct,
            'HQLF': cls.hqlf,
        }
        return SERVICE.get(name)

    @classmethod
    def submit(cls, c):
        """
        Inputs:
        - target: path of work directory,        
        - url: url of task manager,
        - submit_service: a Slurm submit service with args: workdir, file_name
        """
        with OSFS(c['target']) as fs:
            run_infos = []
            run_sh = (c.get('shell') or {}).get('run') or 'run.sh'
            (methods.Mapper(fs).dirs()
             .map(fs.getsyspath)
             .subscribe(lambda d: run_infos.append((d, run_sh))))
            post_sh = (c.get('shell') or {}).get('post') or 'post.sh'
            post_infos = (fs.getsyspath('.'), post_sh)
            service = cls.service(c['submit'])
            if service is not None:
                service(run_infos, post_infos)

    @classmethod
    def sprint(cls, run_infos, post_infos):
        for t in run_infos:
            print('RUN: ', 'DIR: ', t[0], 'FILE: ', t[1])
        print('POST: ', 'DIR: ', post_infos[0], 'FILE: ', post_infos[1])

    @classmethod
    def direct(cls, run_infos, post_infos):
        for t in run_infos:
            cmd = 'cd {dir} && sbatch {file}'.format(dir=t[0], file=t[1])
            with subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE) as p:
                print(p.stdout.read().decode())

    @classmethod
    def hqlf(cls, run_infos, post_infos):
        from dxpy.task.model import creators
        from dxpy.task import interface
        tasks = []
        for i, t in enumerate(run_infos):
            desc = '<PYGATE {0}>.RUN #{1}'.format(post_infos[0], i)
            tasks.append(creators.task_slurm(
                file=t[1], workdir=t[0], desc=desc))
        tasks.append(creators.task_slurm(file=post_infos[1],
                                         workdir=post_infos[0],
                                         desc='<PYGATE {0}>.POST'.format(post_infos[0])))
        depens = [None] * (len(tasks) - 1)
        depens.append(list(range(len(tasks) - 1)))
        g = creators.task_graph(tasks, depens)
        # print('\n'.join([t.to_json() for t in tasks]))
        ids = interface.create_graph(g)
        print('Submitted to HQLF.Task with tids:', ids)


class Cleaner:
    @classmethod
    def msg(cls, fs, rel, verbose=0):
        if verbose is not None and verbose > 1:
            fmt = 'DELETE: {0}/{1}.'
            print(fmt.format(fp.normpath(fs.getsyspath('.')), rel))

    @classmethod
    def rm(cls, fs, path, dryrun):
        if dryrun:
            return
        if fs.isdir(path):
            fs.removetree(path)
        else:
            fs.remove(path)

    @classmethod
    def all(cls, c, is_dryrun):
        exclude = (c.get('clear') or {}).get('keep') or []
        cls.subs(c, is_dryrun)
        with OSFS(c['target']) as fs:
            (methods.files(fs, exclude_files=exclude)
             .do_action(lambda d: cls.msg(fs, d, c.get('verbose')))
             .subscribe(lambda d: cls.rm(fs, d, is_dryrun)))

    @classmethod
    def subs(cls, c, is_dryrun):
        with OSFS(c['target']) as fs:
            (methods.Mapper(fs).dirs()
             .do_action(lambda d: cls.msg(fs, d))
             .subscribe(lambda d: cls.rm(fs, d, is_dryrun)))


def run(target, mac_file, stdout=None, stderr=None):
    warnings.warn('Run method is deprecated', DeprecationWarning)
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
