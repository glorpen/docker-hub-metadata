==============================
Repository Description Updater
==============================

Updates repository description on Docker Hub.

Why?
====

- no api keys available on cloud.docker.com (maybe removed functionality?)
- don't want copy & paste code between projects
- no templating support on Docker Hub side so in some cases no autobuild
- could use Docker Hub hooks but then it becomes like second CI to Travis

Why docker image and not some standalone lib?
---------------------------------------------

If you are using Docker Hub it is highly likley that you are already using containers.
This container is not meant to implement full available API but just enough to don't think about it
when using CI deployment.

Also, if needed, `pandoc` is used to convert your favourite readme markup to MD.

Usage
=====

.. sourcecode::

   usage: docker-description-updater [-h] [--repository NAME] [--username USER]
                                     [--password PASS] [--description DESC]
                                     [--long-description-file LONG_DESC]
                                     [--print-only]
   
   Converts and uploads description to repository on Docker Hub.
   
   optional arguments:
     -h, --help            show this help message and exit
     --repository NAME, -r NAME
                           repository name, eg. glorpen/hub-description-updater
     --username USER, -u USER
     --password PASS, -p PASS
     --description DESC, -d DESC
     --long-description-file LONG_DESC, -l LONG_DESC
                           file with text to convert and send
     --print-only          generate and print text, do not send it to Docker Hub
   
   Use "--" to add arguments to pandoc process, eg. changing output to 10 columns
   wide: docker-description-updater -l README.rst -- --columns 10

Environment variables
---------------------

Env vars correspond to app commandline arguments:

- REPOSITORY
- USERNAME
- PASSWORD
- DESCRIPTION
- LONG_DESCRIPTION_FILE
