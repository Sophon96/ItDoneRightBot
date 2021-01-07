#!/bin/bash

a=$(mktemp /tmp/XXXXXXXXXXXX)
# echo "#!/usr/bin/python3" >> /tmp/$a
echo $1 >> /tmp/$a
chmod +x /tmp/$a
python /tmp/$a
rm /tmp/$a
