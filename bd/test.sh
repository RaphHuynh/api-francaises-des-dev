#!/bin/sh
mysql -uroot -p$MYSQL_ROOT_PASSWORD < /docker-entrypoint-initdb.d/sql/test_user.sql
mysql -uroot -p$MYSQL_ROOT_PASSWORD API_francaises_des_dev_test < /docker-entrypoint-initdb.d/sql/tables.sql