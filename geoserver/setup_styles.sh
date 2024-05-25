#!/bin/bash

if [[ ! -d /opt/geoserver/data_dir/styles/ ]];then
  mkdir -p /opt/geoserver/data_dir/styles/
fi
cp -r /styles/* /opt/geoserver/data_dir/styles/