import os
import sys
import context

class ConfigNamespaceImportContext(object):
    def __enter__(self):
        self.stored_cfg_namespace = context.CFG_NAMESPACE

    def __exit__(self, *args, **kwargs):
        context.set_cfg_namespace(self.stored_cfg_namespace)

def get_env_name():
    env = None #'dev' # the default
    env = os.environ.get('MODE', env)
    if env is None:
        raise Exception("MOED=None")
    env = env.lower()
    return env

def get_env_config(package, pre=False):
    return '%(pkg)s.%(env)s%(pre_env)s' % {
            'pkg': package,
            'env': get_env_name(),
            'pre_env': '_pre' if pre else ""}

def get_context(cfg_namespace=None):
    return context.ctx(cfg_namespace)

LOADED = {}
def load(package='conf', cfg_namespace_to_load='sphinx'):
    global LOADED
    if LOADED.get(cfg_namespace_to_load, False):
        return None
    context.set_cfg_namespace(cfg_namespace_to_load)
    MODULES = [
        # module name, required?
        ('%s.version' % package,   False),
        (get_env_config(package, pre=True), False),
        ('%s.all' % package,       True),
        ('%s.dev' % package,       False),
        (get_env_config(package),  True),
        ('%s.local' % package,     False),
        ]
    ctx = get_context()
    ctx.clear()
    for name, opt in MODULES:
        try:
            if name in sys.modules:
                reload(sys.modules[name])
            else:
                __import__(name)
        except ImportError, e:
            if opt:
                raise

    context.set_cfg_namespace(context.DEFAULT_CFG_NAMESPACE)
    LOADED[cfg_namespace_to_load] = True
