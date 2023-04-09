docker run --name mysql-server -e MYSQL_ROOT_PASSWORD=mysecretpassword -e MYSQL_ROOT_HOST=% -d -p 3306:3306 mysql/mysql-server
