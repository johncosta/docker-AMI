docker-AMI
==========

Scripts used to create docker-AMI images

Using
-----


1) Create the following environment variables in your ``~/.bashrc`` file::

    export AWS_KEY="<your key>"
    export AWS_SECRET="<your secret>"
    export PRIVATE_KEY_NAME="<name of private key>"
    export PATH_TO_PRIVATE_KEY="<path to private key>"
    export PRIVATE_KEY_PASSWORD="<password for key>"


2) Set the following::

    export IMAGE_ID="ami-d0f89fb9"
    export IMAGE_NAME="Ubuntu Server 12.04.2 LTS AMI ID ami-d0f89fb9 (x86_64)"
    export IMAGE_SIZE="25"


3) Build the new image::

    python setup.py install
    build-docker-ami $AWS_KEY $AWS_SECRET "$IMAGE_ID" "$IMAGE_NAME" "$PRIVATE_KEY_NAME" "$PATH_TO_PRIVATE_KEY" "$PRIVATE_KEY_PASSWORD" $IMAGE_SIZE


Additional things to consider:
------------------------------

* Image names are unique.  If the image already exists by name, it will not be recreated.
* Image names AMI names must be between 3 and 128 characters long, and may contain
  letters, numbers, '(', ')', '.', '-', '/' and '_'

AMIs
----

Base Images
+++++++++++

+--------------+-----------------------------------------------------------+ 
| AMI Image ID | Description                                               +
+==============+===========================================================+ 
| ami-d0f89fb9 | Ubuntu Server 12.04.2 LTS AMI ID ami-d0f89fb9 (x86_64)    |
+--------------+-----------------------------------------------------------+
| ami-c30360aa | Ubuntu Server 13.04 AMI ID ami-c30360aa (x86_64)          |
+--------------+-----------------------------------------------------------+

Built Images
++++++++++++

+----------------+--------------+---------------------------------------------------------------------------------+
| Docker Version | AMI Image ID | Description                                                                     +
+================+==============+=================================================================================+
| 0.4.7          | ami-6282f00b | Docker Version (0.4.7) - Ubuntu Server 13.04 AMI ID ami-c30360aa (x86_64)       |
+----------------+--------------+---------------------------------------------------------------------------------+
| 0.4.7          | ami-2a82f043 | Docker Version (0.4.7) - Ubuntu Server 12.04.2 LTS AMI ID ami-d0f89fb9 (x86_64) |
+----------------+--------------+---------------------------------------------------------------------------------+
