#!/usr/bin/env dash

URL="localhost:8080/api/business/test"
COOKIE="dev_appserver_login=test@example.com:True:185804764220139124118"
OPTS="--cookie ${COOKIE}"

curl localhost:8080/api/user/tmp ${OPTS} -X PUT --data "name=tmp"
curl localhost:8080/api/user/tmp2 ${OPTS} -X PUT --data "name=tmp"

echo "PUT ${URL}"
curl ${URL} ${OPTS} --trace tmp -X PUT --data-urlencode "name=tester" --data-urlencode "lat=0" --data-urlencode "lon=0" --data-urlencode 'owners=["tmp"]'

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nPOST ${URL} name=frank"
curl ${URL} ${OPTS} -X POST --data-urlencode "name=frank"

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nPOST ${URL} owners=[\"tmp2\"]"
curl ${URL} ${OPTS} -X POST --data-urlencode 'owners=["tmp2"]'

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nPOST ${URL} owners=[\"faker\"] (fail)"
curl ${URL} ${OPTS} -X POST --data-urlencode 'owners=["faker"]'

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nPOST ${URL} owners=[\"frank\", \"tmp\"] (fail)"
curl ${URL} ${OPTS} -X POST --data-urlencode 'owners=["tmp", "faker"]'

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nPOST ${URL} owners=[\"tmp\", \"tmp2\"] (fail)"
curl ${URL} ${OPTS} -X POST --data-urlencode 'owners=["tmp", "tmp2"]'

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nDELETE ${URL}"
curl ${URL} ${OPTS} -X DELETE

echo "\n\nGET ${URL}"
curl ${URL} ${OPTS} -X GET -f

echo "\n\nDELETE ${URL}"
curl ${URL} ${OPTS} -X DELETE

curl localhost:8080/api/user/tmp2 ${OPTS} -X DELETE
curl localhost:8080/api/user/tmp ${OPTS} -X DELETE
