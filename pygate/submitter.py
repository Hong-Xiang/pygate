class Submitter:
    def __init__(self, fs, config):
        from .utils import sub_dir_filters
        self.fs = fs
        self.c = config['submit']
        self.sub_dirs = sub_dir_filters(config)
        self.map_file = config['shell']['map']['output']
        self.merge_file = config['shell']['merge']['output']

    def _get_map_info(self):
        from dxpy.batch import DirectoriesFilter
        return [(self.fs.getsyspath(d), self.map_file) for d in DirectoriesFilter(self.sub_dirs).lst(self.fs)]

    def _get_merge_info(self):
        return (self.fs.getsyspath('.'), self.merge_file)

    def submit(self):
        run_infos = self._get_map_info()
        merge_infos = self._get_merge_info()
        if self.c['worker'] == 'slurm':
            self._slurm(run_infos, merge_infos)
        elif self.c['worker'] == 'hqlf':
            self._hqlf(run_infos, merge_infos)

    def _echo(self, info, fout):
        msg = '\t'.join([str(e) for e in info])
        print(msg)
        print(msg, file=fout)

    def _slurm(self, run_infos, post_infos):
        from dxpy.slurm import sbatch
        sids = []
        with self.fs.open(self.c['output'], 'w') as fout:
            for t in run_infos:
                sid = sbatch(t[0], t[1])
                self._echo(('MAP', sid, t[0], t[1]), fout)
                sids.append(sid)
            sids = [str(s) for s in sids]
            deparg = '--dependency=afterok:' + ':'.join(sids)
            sid = sbatch(post_infos[0], post_infos[1], deparg)
            self._echo(('MERGE', sid, post_infos[0], post_infos[1]), fout)

    def _hqlf(self, run_infos, post_infos):
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
        with self.fs.open(self.c['output'], 'w') as fout:
            print('Submitted via HQLF, with tids:', file=fout)
            print(ids, file=fout)
