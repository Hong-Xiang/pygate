
Installation
============

How to get pygate and configuration
-----------------------------------

* if you want to run *pygate* locally,you should following the steps:

    1. We put the source on the `Github`_.You may need an Github account to clone or downoald the files.Here is the `Github Guides`_.

    2. Ensure your python3 version is the most current version.
        + We recommand *Anaconda* to get `python3`.Here is the `Anaconda`_.
        + The Anaconda should be set into syspath. 
        + ``source ~/.bashrc`` or reboot the terminal to update bashrc.
        + ``$ python --version`` and get the output ``Python 3.6.4 :: Anaconda custom(64-bit)`` (for now).

    3. Install *pygate*   

        + ``pip install dxl-pygate``

    4. Ensure *GATE* is installed and configured already. 
    
    5. You have already installed *pygate*.Go to the :ref:`First step of pygate`.

* if you are an external member(you haven gotten an account),you can run on the server:
    
    1. Install *Anaconda* to get latest `python3` in your work folder.The recommanded path with high performance is ``/mnt/Gluster_NoGPU/usr``.

    2. Ensure your python3 version is the most current version.
        + We recommand *Anaconda* to get `python3`.Here is the `Anaconda`_.
        + The Anaconda should be set into syspath. 
        + ``source ~/.bashrc`` or reboot the terminal to update bashrc.
        + ``$ python --version`` and get the output ``Python 3.6.4 :: Anaconda custom(64-bit)`` (for now).
    
    3. Install *pygate*   

        + ``pip install dxl-pygate``
    
    4. Configured *GATE*
        + ``soure/hqlf/softewares/moudle/simu8.0.sh``

    5. You have made *pygate* ready.Go to the :ref:`First step of pygate`.

    .. note::
     We will get the environment set up and configured on each node of the server.
     You need to install and configure the environment in your own work folder at present.
      
    


.. _Github: https://github.com/Hong-Xiang/pygate.git
.. _Github Guides: https://guides.github.com/activities/hello-world
.. _Anaconda: https://www.anaconda.com/download/#linux