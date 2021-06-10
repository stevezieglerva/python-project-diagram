chsum1=""

while [[ true ]]
do
    chsum2=`find . -type f -mtime -2s -prune -exec md5 {} \;`
    if [[ $chsum1 != $chsum2 ]] ; then           
        . run_tests.sh
        chsum1=$chsum2
    fi
    sleep 2
done