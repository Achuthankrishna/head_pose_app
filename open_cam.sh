#!/bin/bash
chmod 666 /dev/video0

# Grant access to camera device and then execute the command
exec "$@"
