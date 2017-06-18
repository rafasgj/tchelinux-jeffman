#!/bin/sh

if [ $# -ne 1 ]
then
    echo -e "\nusage:\n\t mkevent <codiname>\n"
    exit 1
fi

base="`dirname $0`"

codiname=$1
shift

echo "Creating event: ${codiname}"

if ! "$base/tchelinux-event.py" ${codiname}
then
    echo "Failed to generate hotsite."
    exit 1
fi

[ -d ${codiname} ] && rm -rf ${codiname}
mkdir -p ${codiname}/data
mv CNAME index.html ${codiname}
cp -r template/* ${codiname}
[ -d "images" ] && cp -r images ${codiname} || mkdir ${codinome}/images
cp data/${codiname}.json ${codiname}/data/${codiname}.json

