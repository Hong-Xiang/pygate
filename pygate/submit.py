class Submitter:
    """
    Submit jobs.
    """

    def __init__(self, config, root_fs):
        """
        Inputs:
            config: dict, consists of two script.                
                pattern:
                    sub directories pattern
                map_script:
                    scripts to run in each directories
                merge_script: (only supported when using HQLF submitter)
                    will run after all map tasks.
                method:
                    one of following methods:
                        PRINT: print scirpts,
                        SLURM: submit to slurm,
                        HQLF: submit to hqlf system

        """
        self.c = config
        self.fs = root_fs

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
