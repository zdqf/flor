Install Flor
=================

1. **Clone or download this repository.** ``git clone https://github.com/ucbrise/flor``
2. **Create a Virtual Environment.**
 * Download anaconda `here <https://www.anaconda.com/download/>`. Be sure to get Python 3.6 or higher.

 * Create a new environment using the command: ``conda create --name [env_name]``.

 * Activate your new environment using: ``source activate [env_name]``.

 * Once you have activated your environment, run the command: ``pip install -r requirements.txt``.

 * Be sure that you have GraphViz by running the following command: ``brew install graphviz``.

 *Note: Whenever you work with Flor, make sure that this environment is active. For more information about environments, please read `this guide <https://conda.io/docs/user-guide/tasks/manage-environments.html>`.*

3. **Installing Ray (Flor Dependency)**

 * Run the following Brew Commands:

 ``brew update``
 ``brew install cmake pkg-config automake autoconf libtool boost wget``
 *Note: Linux users should use linuxbrew. See installation details in the **Additional Linux Instructions** section.*

 * Run the following Pip Commands:

 ``pip install numpy funcsigs click colorama psutil redis flatbuffers cython --ignore-installed six
 conda install libgcc
 pip install git+https://github.com/ray-project/ray.git#subdirectory=python``

 * If the command above fails, then use: ``pip3 install ray``.

4. **Add Flor to Bash Profile**
 * Open Bash Profile using the following MacOS command:
 ``vim  ~/.bash_profile``
 *Note: linux machines should use `vim ~/.bashrc`*

 * Add the path to your flor directory in your Bash Profile. Here is an example of a command to add.
 ``export PYTHONPATH="$PYTHONPATH:/Users/Sona/Documents/Jarvis/flor"``

5. **Installing Ground**

 * Download the zip file containing the latest version of Ground `here <https://github.com/ground-context/ground/releases>` and unzip it.
 
 * Create a file called ``script.sh`` within the unzipped *ground-0.1.2/db* folder. 

 * Inside ``script.sh``, add a path to the *ground-0.1.2/db/postgres_setup.py* file followed by ``ground ground drop``. Here is an example of the lines to add to ``script.sh``:

 ``
 #!/bin/bash 
 `
 `
 python3 /Users/Bob/ground-0.1.2/db/postgres_setup.py 
 ground ground drop
 ``


 * Open your bash profile using the following MacOS command: ``vim  ~/.bash_profile``

 *Note: linux machines should use ``vim ~/.bashrc``*

  * Add the following command to your Bash Profile:
	``alias startground='bash /Users/Sona/ground-0.1.2/db/myscript.sh && bash /Users/Sona/ground-0.1.2/bin/ground-postgres'``

 * To update your Bash Profile, run: ``source ~/.bash_profile``
	*Note: linux users should use ``source ~/.bashrc``*

 * Linux machines may require several more steps to get ground working. See **Additional Linux Instructions**.

6. **Installing Grit and Client**

 * Flor requires ground-context in order to operate properly. Go to the `Ground Context Repo <https://github.com/ground-context>` and download/install the Grit and Client repos. Downloading the zip files and unzipping them is sufficient. 

 * Open Bash Profile using the following MacOS command: ``vim  ~/.bash_profile``

 * Modify the bash_profile to include paths to these directories like the following commands:

 ``export PYTHONPATH="$PYTHONPATH:/Users/Sona/Documents/Jarvis/grit-master/python/"
 export PYTHONPATH="$PYTHONPATH:/Users/Sona/Documents/Jarvis/client-master/python/"``

 * To update your Bash Profile, run the following command: ``source ~/.bash_profile``

7. **Starting Ground**

 * In order to use Flor, you will need to start Ground. In your environment, run the following command:
 ``startground``


For examples on how to write your own flor workflow, please have a look at:
``
examples/twitter.py -- classic example
examples/plate.py -- multi-trial example
``

Make sure you:
1. Import `flor`
2. Initialize a `flor.Experiment`
2. set the experiment's `groundClient` to 'git'.

Once you build the workflow, call `pull()` on the artifact you want to produce. You can find it in `~/flor.d/`.

If you pass in a non-empty `dict` to `pull` (see `lifted_twitter.py`), the call will return a pandas dataframe with literals and requested artifacts for the columns, and different trials for the rows.

## Additional Linux Instructions
 * **Installing linuxbrew**
 	* Use the command:
 		`sudo apt install linuxbrew-wrapper`
 	* After installation, follow the additional steps to make sure dependencies are installed and brew is added to path.

 		`Sudo apt-get install build-essential
		Echo ‘export PATH=”/home/linuxbrew/.linuxbrew/bin:$PATH”’ >>~/.bash_profile
		Echo ‘export MANPATH=”/home/linuxbrew/.linuxbrew/share/man:$MANPATH”’ >>~/.bash_profile
		Echo ‘export INFOPATH=”/home/linuxbrew/.linuxbrew/share/info:$INFOPATH”’ >>~/.bash_profile
		PATH=”/home/linuxbrew/.linuxbrew/bin:$PATH”
		Brew install gcc`
 * **Bash Profile**
 	* Where specified, linux machines should use `~/.bashrc` instead of `~/.bash_profile`

 * **Additional Ground Instructions**
 	* Postgres is needed for ground to run. Use the following command to download and install the latest version of postgres.
 		`sudo apt install postgresql`

 	* Open `pg_hda.conf`, which can be located in `/etc/postgresql/<version>/main/`.
 		* under the section `"local" is for Unix domain socket connections only`, set METHOD to `trust`

 		* under IPv4 local connections, add an entry that looks like:
 			`host      ground     ground    127.0.0.1/32    trust`

 		* comment out all lines below the section 
 		`Allow replication connections from localhost...`

 	* Create the `ground` user and `ground` database.
 		* Create the user by using the command 
 		`sudo -u postgres createuser ground`

 		* Create a database by opening postgres with 
 		`sudo -i -u postgres` 
 		and issuing the command 
 		`createdb ground`
 	* You should now be able to enter the `ground-0.1.2/db` directory and issue the `startground` command.