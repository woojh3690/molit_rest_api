readonly program='rest'
get_status()

{

    ps ux | grep ${program} | grep -v grep | awk '{print $2}'

}
PID=$(get_status)
if [ -n "${PID}" ]; then

   kill -9 ${PID}
   echo "${program} End"
        exit 0
else

   echo "${program} is not running "

fi

