#!/usr/bin/env bash
# Installs the editing tools for the Brooklyn Vice pipeline (Ubuntu 24.04).
# OpenShot editor + libopenshot Python bindings + ffmpeg.
# Note: libopenshot is built for Python 3.12. Run scripts with python3.12.
set -euo pipefail
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openshot-qt python3-openshot ffmpeg
python3.12 -c "import openshot; print('libopenshot', openshot.OPENSHOT_VERSION_FULL)"
