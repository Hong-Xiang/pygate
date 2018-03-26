.. _Command List:

Here is the command list of *pygate*
====================================
* ``pygate``
    + ``analysis``
        - ``predefined``
        - ``script``
    + ``clean``
    + ``generate``
        - ``cfg``
        - ``mac``
            * ``predefined``
            * ``script``
        - ``mac_template``
        - ``shell``
    + ``init``
        - ``auto``
        - ``bcast``
        - ``ext``
        - ``subdir``
    + ``merge``
    + ``submit``


$ pygate 
---------
Usage: pygate [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config TEXT  config file name
  --no-config        ignore config file
  --dryrun           Do not do anything, just show expected results.
  --help             Show this message and exit.

Commands:
::
  analysis
  clean
  generate
  init
  merge
  submit


$ pygate analysis 
------------------
Usage: pygate analysis [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
::
  predefined
  script


$ pygate analysis predefined
----------------------------
Usage: pygate analysis predefined [OPTIONS]

Options:
  -n, --name TEXT    Predefined analysis type name.
  -s, --source TEXT  Analysis source data filename.
  -o, --output TEXT  Analysis target data filename.
  --help             Show this message and exit.


$ pygate analysis script
------------------------
Usage: pygate analysis script [OPTIONS]

Options:
  -t, --target TEXT  Analysis .py filename.
  -s, --source TEXT  Analysis source data filename.
  -o, --output TEXT  Output filename.
  --help             Show this message and exit.


$ pygate clean
--------------
Usage: pygate clean [OPTIONS]

Options:
  -d, --subdirectories   remove subdirectories
  -f, --root-files TEXT  remove files in work directory
  -s, --slurm-outputs    remove *.out *.err files
  --help                 Show this message and exit.


$ pygate generate
-----------------
Usage: pygate generate [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
::
  cfg           Generate initial config file.
  mac           Generate mac file.
  mac_template
  shell         Generate shell script, pre run or post run.


$ pygate generate cfg
---------------------
Usage: pygate generate cfg [OPTIONS]

  Generate initial config file.

Options:
  -t, --target TEXT  Config file name.
  -f, --format TEXT  Format of config file, json or yml
  --help             Show this message and exit.


$ pygate generate mac 
---------------------
Usage: pygate generate mac [OPTIONS] COMMAND [ARGS]...

  Generate mac file.

Options:
  --help  Show this message and exit.

Commands:
::
  predefined  Generate mac file by predefined system.
  script      Generate mac file by running a .py file.


$ pygate generate mac predefined
--------------------------------
Usage: pygate generate mac predefined [OPTIONS]

  Generate mac file by predefined system.

Options:
  -p, --predefined TEXT  Name of predefined system to generate mac file.
  -c, --config TEXT      config filename to generate macs.
  -t, --target TEXT      MAC filename, will passed to script or predefined
                         method.
  --help                 Show this message and exit.


$ pygate generate mac script
----------------------------
Usage: pygate generate mac script [OPTIONS]

  Generate mac file by running a .py file.

Options:
  -t, --target TEXT  Filename of script to run to generate mac file.
  -c, --config TEXT  config filename to generate macs.
  -o, --output TEXT  MAC filename, will passed to script or predefined method.
  --help             Show this message and exit.


$ pygate generate mac_template
-------------------------------
 Usage: pygate generate mac_template [OPTIONS]

Options:
  -f, --filename TEXT  Show the file name.
  --help               Show this message and exit.


$ pygate generate shell
-----------------------
Usage: pygate generate shell [OPTIONS]

  Generate shell script, pre run or post run.

Options:
  --help  Show this message and exit.


$ pygate init
-------------
Usage: pygate init [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
::
  auto
  bcast
  ext     Copy external files.
  subdir


$ pygate init auto 
-------------------
Usage: pygate init auto [OPTIONS]

Options:
  --mac-auto
  --mac-no-create
  --mac-force-create
  --help              Show this message and exit.


$ pygate init bcast
--------------------
Usage: pygate init bcast [OPTIONS]

Options:
  -t, --target INTEGER  Files to broadcast to subdirectories.
  -e, --no-ext          Include all external files.
  --help                Show this message and exit.


$ pygate init ext
-----------------
Usage: pygate init ext [OPTIONS]

  Copy external files.

Options:
  --help  Show this message and exit.


$ pygate init subdir
--------------------
Usage: pygate init subdir [OPTIONS]

Options:
  -n, --nb-split INTEGER  Number of subdirectories.
  -f, --sub-format TEXT   Subdirectories format str.
  --help                  Show this message and exit.


$ pygate merge
---------------
Usage: pygate merge [OPTIONS]

Options:
  -t, --target TEXT  Target str.  
  -m, --method TEXT  Method str. 
  --help             Show this message and exit.


$ pygate submit
---------------
Usage: pygate submit [OPTIONS]

Options:
  -b, --broadcast TEXT  Broadcast file str.  
  -s, --single TEXT     Single str. 
  --help                Show this message and exit.


  