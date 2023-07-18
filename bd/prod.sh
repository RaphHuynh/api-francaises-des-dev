#!/bin/sh
mysql -uroot -p$MYSQL_ROOT_PASSWORD < /docker-entrypoint-initdb.d/sql/prod_user.sql
mysql -uroot -p$MYSQL_ROOT_PASSWORD API_francaises_des_dev < /docker-entrypoint-initdb.d/sql/tables.sql