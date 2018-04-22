#!/usr/bin/env bash


celery -A sv_core worker -l info -B -E &
