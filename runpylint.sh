#!/bin/bash
pylint --load-plugins pylint_django -f colorized --rcfile=pylint.cfg --disable=I0011 -j 4 -r n django_logutils/

