#!/usr/bin/env bash

tmux new-session -d -s "CeleryWorker" deploy/worker.sh
