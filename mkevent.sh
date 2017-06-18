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

"$base/tchelinux-event.py" ${codiname}

[ -d ${codiname} ] && rm -rf ${codiname}
mkdir ${codiname}
mv CNAME index.html ${codiname}
cp -r template/* ${codiname}
[ -d "images" ] && cp -r images ${codiname} || mkdir ${codinome}/images

