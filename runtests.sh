#!/bin/bash
coverage run --source django_logutils -m py.test -v
coverage report -m

