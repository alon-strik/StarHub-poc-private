#!/bin/bash
(./$1) | ssh -t -t admin@192.168.122.146
