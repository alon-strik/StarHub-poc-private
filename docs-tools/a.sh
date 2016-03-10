#!/bin/bash
echo config system central-management
sleep 1
echo   set type fortimanager
sleep 1
echo   set fmg 10.0.5.90
sleep 1
echo   set include-default-servers disable
sleep 1
echo   config server-list
sleep 1
echo     edit 1
sleep 1
echo       set server-type update
sleep 1
echo       set server-address 10.0.5.90
echo     end
sleep 1
echo end
sleep 1
