#######
# CONFIG SETUP do not change or configs will break
#    this goes a the top of any config file. it adds stuff to the global config
#    context. 
import context
cfg = context.ctx()
cfg.push(__name__)
# END CONFIG SETUP
#######
import os

_RUNPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

#not sure if any of these are being used ???
cfg.mode = 'prod'


