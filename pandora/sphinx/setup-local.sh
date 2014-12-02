dir=$(dirname $0)
venv=venv.local

virtualenv $dir/$venv
source $dir/$venv/bin/activate
pip install -r $dir/requirements.txt
deactivate
