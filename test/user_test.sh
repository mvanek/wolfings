#!/usr/bin/env dash

URL="localhost:8080/api/user/test"
COOKIE="dev_appserver_login=test@example.com:True:185804764220139124118"
OPTS="--cookie ${COOKIE}"

echo "PUT ${URL} name=tester"
curl ${URL} ${OPTS} -X PUT --data "name=tester"

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nPOST ${URL} name=frank"
curl ${URL} ${OPTS} -X POST --data "name=frank"

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nDELETE ${URL}"
curl ${URL} ${OPTS} -X DELETE

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f
