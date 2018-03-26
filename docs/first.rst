.. _first step of pygate:

First step of pygate
====================

In this page,we will run a example consists of two steps;

.. _file generators:

1. File ``main.mac`` generates.
--------------------------------

* Before a *GATE* process,we generally need to make a file of ``main.mac`` ,
in which we can set the compomnents( *world,system,phantom,soure and digitizer etc.* ) for *GATE* simulation.

* The question is that the definition of compomnents is too heavy and complicated.
  A lot of time and ennergy wastes on this.

* *Pygate* offers a function of **File Gnetators** .Users can confirured the compomnents easily 
  by set several arguments of neccessary compomnents you want in a file of ``make_mac.py`` (you can name it freely).
  A file of ``mac.yml`` may needed containing some default settings of the ``main.mac`` ,or you can set these in ``make_mac.py`` directly.

* The command for ``main.mac`` generating is:
    + ``$ pygate generate mac script -t make_mac.py -o main.mac -c mac.yml`` .
    + ``make_mac.py`` and ``mac.yml`` should be included in current work folder.
    + Then you will find the ``main.mac`` in the folder.

* The main work for this step is to code ``make_mac.py`` .Usres can modify on the template for first time.
:ref:make_mac.py

.. _subsystem:

2. Submit a task to subsystem
------------------------------
* Usually there are hundreds of millions,even billions events occuring during a *GATE* simulation,which is the reason why the process take a long time.
* However,it a repetable work for a *GATE* program to generate an event.*Pygate* offers a method to speed up the process.*Pygate* divides the task into a lot of parts,
* then submits these parts to server.Each part of the original task will be distributed to no-wroking machine of the net by *SLurm*.Thus,we get a very high speed for *GATE* simulation. 
* Users should know the following steps to archive it:
    1. Users should get the needed configured files by excuting this command: ``$ pygate ini ext`` .You will get the files in folder: 
        * ``main.mac`` ,you get it last in the fomer.
        * ``GateMaterials.db`` ,significant file for *GATE* configuration,can't be lack.
        * ``Hits2CSV.C`` ,may needed if you want the data of *csv* format.
        * ``Materials.xml``
        * ``Surface.xml`` ,set the surface rendering.Or you can seclect volume rendering.
        
    #. When you get the neccessary files in the work folder,you need to divide the task into parts.
        * ``$ pygate init subdir -n --INTGER -f --STR`` ,you can set the number of parts and the name of subdirectories as you want.The default option is "sub.[10]" and you will get 10 subdirectories of "sub.[x]"(x~[0-10]).
        * ``$ pygate init bcast`` ,broadcast the files to subdirectories maken last step.
        * ``$ pygate generate shell`` ,generate *run.sh* for *SLurm* to distribute the task and *post.sh* to merge the results of each parts.
        * ``$ pygate submit`` ,submit the task to subsystem. *SLurm* will do the disribution.The details information of disribution will print on the screen.You can easily know which machine each part run.
        * There are two procedures before getting results:
            + First,the machines absorbs the mission and complete it,then feedback the results to subdirectories. ``run.sh`` is for this step.
            + Then the results from subdirectories are merged into one file of ``optical.root`` ,containing all collected data of Hits. ``post.sh`` is for this. 






You can refer the detail of commands in :ref:`Command List`