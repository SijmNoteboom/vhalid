# VHALID 
Automated analysis of ROTEM data

Make sure that the "home" location in the python venv/pyvenv.cfg is set to the base interpreter for python. 
1) Open anaconda prompt and type in "where python"
2) Open the venv/pyvenv.cfg file with notepad
2) Copy the return of 1) after the "home" keyword. For me the file looks like this:

home = C:\Users\Sijm.Noteboom\Anaconda3\python.exe
include-system-site-packages = false
version = 3.8.8


# To pack environment for VM:

In anaconda prompt:
$ conda activate vhalid_env
$ conda pack -n vhalid_env
$ conda pack -n vhalid_env -o out_name.tar.gz
$ conda pack -p Anaconda\envs\vhalid_env   # check respective path (C:\Users\User\)
# the file to export is in the path where you ran the last command

# To unpack environment in VM
In anaconda prompt:
$ mkdir -p vhalid_env
$ tar -xzf vhalid_env.tar.gz -C vhalid_env
$ ./vhalid_env/bin/python (in Linu
$ source vhalid_env/bin/activate # (or conda activate vhalid_env)
$ conda-unpack
$ ipython --version
$ source vhalid_env/bin/deactivate # (or conda deactivate)