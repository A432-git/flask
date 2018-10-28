#!/bin/bash
rm -f result.txt
cat iplist.txt | fping > result.txt
