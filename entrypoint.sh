#!/bin/bash
set -e

# DB待ち
/entrypoint/wait-for-it.sh db:3306

# 開発サーバ立ち上げ
python3 manage.py runserver 0.0.0.0:8000