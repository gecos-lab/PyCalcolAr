# PyCalcolAr #

__Ar/Ar geochronology in Jupyter__


## Installing ##

1) Install Anaconda for your system (either Windows, MacOS or Linux) from the [Anaconda installation page](https://www.anaconda.com/products/individual).

Some alternatives are available for MacOS and Linux, but not supported.

Important: insall as standard user, NOT as adminstrator (if the PC has more than one user, each one must have its own Anaconda environment).

2) Install GIT for your system (either Windows, MacOS or Linux) from [Atlassian](https://www.atlassian.com/git/tutorials/install-git) (the company running BitBucket), and create user with your institutional email at [BitBucket](https://bitbucket.org).

3) On Windows you can add a right-click command to run Jupyter Notebook and Jupyter Lab (recomended) in a particular directory (e.g. the PyCalcolAr directory) by merging [these keys]() in the Windows registry.


## Sync/backup with GIT ##

If you use GIT from command line (suggested), the most important commands are the following. If you installed [GIT for Windows](https://gitforwindows.org), you will find a tool to run GIT Bash in a given directory with a right click in Explorer.

To REGISTER your user name and password use the following commands. Do this the first time to avoid being asked for password every time. 

```
git config --global user.name 'your username'
git config --global user.password 'your password'
```
Use `--global` if you want to set user/password for all git projects, or `--local` if you like to set them just for one repository.

To CLONE locally a remote repository (e.g. PyCalcolAr), run the following command in the directory where you want the repository to be hosted (a nuw sub-directory with the repository name will be created here).

```
git clone <remote repository URL>
```

To pull changes FROM remote repository TO the local one, run the following command in the root directory of your local repository.

```
git pull
```

To push changes TO remote repository FROM the local one, run the following sequence of commands in the root directory of your local repository.

```
git add -A
git commit -m "<message for this commit>"
$ git push origin master
```
The first line "stages" the changes you have done to your local files to be "committed". The second line "commits" these changes (registers them as valid and confirmed, with some note added in the "message"). The third line actually pushes the changes to the remote repository (in the "master" branch).

More tutorials on GIT can be found at [Atlassian](https://www.atlassian.com/git/tutorials) or with [Google](www.google.com).

## Process Ar/Ar data with PyCalcolAr ##


