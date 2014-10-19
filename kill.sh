#!/bin/bash

ps aux |grep python3 |grep -v 8080 | awk '{print $2}'|xargs kill -9
