#!/bin/bash

set -e

ctx logger info "Env : ${user}, Env : ${host_string}, Env : ${password}, Env : ${configFile}"

ctx logger info "scp ${configFile} $user@${host_string}:fgt_restore_config"

