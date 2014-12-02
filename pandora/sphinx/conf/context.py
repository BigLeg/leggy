import os
class LazyLoader(object):
    def __init__(self, load_func):
        self.load_func = load_func
        self._loaded = False
        self.val = None

    def __get__(self, obj, objtype):
        if not self._loaded:
            self.val = self.load_func()
            self._loaded = True
        return self.val

class ConfigContext(object):
    __slots__ = ['_stack', '_levels']

    def __init__(self, *args, **kwargs):
        self._stack  = []
        self._levels = []

    def push(self, name):
        self._levels.append(name)
        self._stack.append({})

    def __setattr__(self, name, value):
        if name in ConfigContext.__slots__:
            object.__setattr__(self, name, value)
            return None
        self._stack[-1][name] = value

    def __getattr__(self, name):
        if name in ConfigContext.__slots__:
            return object.__getattribute__(self, name)
        for stk in self._stack[::-1]:
            if name in stk:
                return stk[name]
        raise AttributeError(name)

    def setdefault(self, name, value):
        try:
            getattr(self, name)
        except AttributeError, e:
            self.__setattr__(name, value)
        else:
            pass

    def clear(self):
        self._stack = []
        self._levels = []

    def info(self, name):
        data = {}
        rows = zip(self._levels, self._stack)
        for lvl, stk in rows[::-1]:
            data[lvl] = stk.get(name, '__undefined__')
        return data

    def has(self, name):
        for stk in self._stack[::-1]:
            if name in stk:
                return True
        return False

    def print_info(self, name):
        info = self.info(name)
        for lvl in self._levels[::-1]:
            data = info[lvl]
            print '%s %s' % (lvl, data)

    def iteritems(self):
        return iter((key, getattr(self, key)) for key in self.iterkeys())

    def iterkeys(self):
        seen = set({})
        for stk in self._stack[::-1]:
            for key in stk.viewkeys():
                if key not in seen:
                    yield key
                    seen.add(key)

    # This definition surfaces the members returned by __getattr__ to dir(),
    # which allows us to get tab-completion of members in ipython.
    def __dir__(self):
        return list(self.iterkeys())

    @classmethod
    def lazy_load(cls, name, load_func):
        setattr(cls, name, LazyLoader(load_func))

CONF_CONTEXT = {}
CFG_NAMESPACE = 'sphinx'
DEFAULT_CFG_NAMESPACE = 'sphinx'
def ctx(cfg_namespace=None):
    if cfg_namespace:
        return CONF_CONTEXT[cfg_namespace]

    if CONF_CONTEXT.get(CFG_NAMESPACE, None) is None:
        CONF_CONTEXT[CFG_NAMESPACE] = ConfigContext()
    return CONF_CONTEXT[CFG_NAMESPACE]

def set_cfg_namespace(cfg_namespace):
    global CFG_NAMESPACE
    CFG_NAMESPACE = cfg_namespace
