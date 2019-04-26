import pickle as cloudpickle

from .scanner_type import ScannerType

class ActualParam(ScannerType):
    """
    Collects from the actual parameters passed into a function
    For the context-specific call to that function, not every invocation of that function
    """

    def __init__(self, name, file_path, class_ctx, func_ctx, prev_lsn, func_name, pos_kw):
        """

        :param file_path: file path of pre-annotated source where the highlight appears
        :param class_ctx: ...
        :param func_ctx: the function or root context (e.g.  None) where this highlight appears.
                    a.k.a. the context of the prev_lsn
        :param prev_lsn: The lsn of the log statement that statically immediately precedes the highlight
                            the purpose is to narrow the scope of search and limit possibility of ambiguities
        :param follow_lsn: ...
        :param func_name: The name of the function that the highlighted actual param is passed to
        :param pos_kw: {'pos': int} or {'kw': str} ... To resolve the value of the parameter
        """
        super().__init__(name, file_path, class_ctx, func_ctx, prev_lsn)
        self.func_name = func_name
        self.pos_kw = pos_kw

        # State
        self.func_enabled = False

    def _get_strict_ancestors(self, contexts):
        assert len(contexts) >= 2
        parent = contexts[-2].parent_ctx
        if len(contexts) >= 3:
            pred = contexts[-3]
        else:
            pred = None
        return parent, pred


    def _ancestor_is_enabled(self, contexts):
        if contexts:
            ctx = contexts[-1].parent_ctx
            if len(contexts) >= 2:
                while ctx not in self._get_strict_ancestors(contexts):
                    if ctx.is_enabled(self):
                        return True
                    ctx = ctx.parent_ctx
            else:
                while ctx is not None:
                    if ctx.is_enabled(self):
                        return True
                    ctx = ctx.parent_ctx
        return False

    def consume_func_name(self, log_record, trailing_ctx, contexts):
        if 'start_function' in log_record:
            if log_record['start_function'] == self.func_name:
                self.func_enabled = True
                # print("func enabled")
            elif log_record['start_function'] == '__init__' and trailing_ctx.class_ctx == self.func_name:
                self.func_enabled = True
                # print("func_enabled")
        elif 'end_function' in log_record:
            if log_record['end_function'] == self.func_name:
                self.func_enabled = False
                # print("func_disabled")
            elif log_record['end_function'] == '__init__' and contexts[-1].class_ctx == self.func_name:
                self.func_enabled = False
                # print("func_disabled")

    def consume_data(self, log_record, trailing_ctx, contexts):
        """

        :param log_record: dict from log
        :return:
        """
        # data log record
        if trailing_ctx is not None and trailing_ctx.is_enabled(self):
            if log_record['lsn'] == self.prev_lsn:
                self.prev_lsn_enabled = True
                # print("prev_lsn_enabled")
            elif log_record['lsn'] == self.follow_lsn:
                self.prev_lsn_enabled = False
                # print("prev_lsn_disabled")
        ffflag = self.prev_lsn_enabled and self.func_enabled
        _ = ffflag or True
        if self._ancestor_is_enabled(contexts) and \
                self.prev_lsn_enabled and self.func_enabled:
            # print("collecting...")
            # active only means search
            if 'params' in log_record:
                params = []
                unfolded_idx = 0
                for param in log_record['params']:
                    # param is a singleton dict. k -> value
                    k = list(param.keys()).pop()
                    idx, typ, name = k.split('.')
                    if typ == 'raw':
                        params.append({k: cloudpickle.loads(eval(param[k]))})
                        unfolded_idx += 1
                    elif typ == 'vararg':
                        list_of_params = cloudpickle.loads(eval(param[k]))
                        for each in list_of_params:
                            new_key = '.'.join((str(unfolded_idx),'raw','$'))
                            params.append({new_key: each})
                            unfolded_idx += 1
                    elif typ == 'kwarg':
                        dict_of_params = cloudpickle.loads(eval(param[k]))
                        for k in dict_of_params:
                            new_key = '.'.join(('$','raw',k))
                            params.append({new_key: dict_of_params[k]})
                    else:
                        raise RuntimeError()

                #params: List[Singleton_Dict[(idx, 'raw', kw_name), deserialized_val]]

                if 'pos' in self.pos_kw:

                    for single_dict in params:
                        k = list(single_dict.keys()).pop()
                        if int(k.split('.')[0]) == self.pos_kw['pos']:
                            return single_dict
                else:
                    assert 'kw' in self.pos_kw
                    for single_dict in params:
                        k = list(single_dict.keys()).pop()
                        if k.split('.')[2] == self.pos_kw['kw']:
                            return single_dict



