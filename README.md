# PyCalcolAr #

__ Ar/Ar geochronology in Jupyter __



## Installing ##

1) Install Anaconda for your system (either Windows, MacOS or Linux) from the [Anaconda installation page](https://www.anaconda.com/products/individual). Some alternatives are available for MacOS and Linux, but not supported.

Important: insall as standard user, NOT as adminstrator (if the PC has more than one user, each one must have its own Anaconda environment).

2) Install GIT for your system (either Windows, MacOS or Linux) from [Atlassian](https://www.atlassian.com/git/tutorials/install-git) (the company running BitBucket), and create an account with your institutional email at [BitBucket](https://bitbucket.org).

3) On Windows you can add a right-click command to run Jupyter Notebook and Jupyter Lab (recomended) in a particular directory (e.g. the PyCalcolAr directory) by merging [the keys that you can download from here](raw/helpers/Jupyter_right_click.zip).


## Sync/backup with GIT ##

If you use GIT from command line (recomended), the most important commands are the following. If you installed [GIT for Windows](https://gitforwindows.org), you will find a tool to run GIT Bash in a given directory with a right click in Explorer.

To REGISTER your user name and password use the following commands. Do this the first time to avoid being asked for password every time. 

```
git config --global user.name 'your username'
git config --global user.password 'your password'
```
Use `--global` if you want to set user/password for all git projects, or `--local` if you like to set them just for one repository.


To CLONE locally a remote repository (e.g. PyCalcolAr), run the following command in the directory where you want the repository to be hosted (a nuw sub-directory with the repository name will be created here). This command line can be copied from the "clone" icon in the repository home page. You can clone the repository wherever yoy like on your machine.

```
git clone https://andrebis@bitbucket.org/andrebis/pycalcolar.git
```
Use another URL in case you are cloning another repository.


To pull changes FROM remote repository TO the local one, run the following command in the root directory of your local repository (e.g. C://<some path>/pycalcolar).

```
git pull
```


To push changes TO remote repository FROM the local one, run the following sequence of commands in the root directory of your local repository (e.g. C://<some path>/pycalcolar).

```
git add -A
git commit -m "<message for this commit>"
$ git push origin master
```
The first line "stages" the changes you have done to your local files to be "committed". The second line "commits" these changes (registers them as valid and confirmed, with some note added in the "message"). The third line actually pushes the changes to the remote repository (in the "master" branch).

More tutorials on GIT can be found at [Atlassian](https://www.atlassian.com/git/tutorials) or with [Google](www.google.com).

## Process Ar/Ar data with PyCalcolAr ##

Navigate to the root directory of your local PyCalcolAr repository (wherever you have cloned it, e.g. C://<some path>/pycalcolar), right-click and select "Jupyter Lab" (recomended) or "Jupyter Notebook", and Jupyter will open in your web browser. Open the "notebooks" directory and run a notebook with a double click.

