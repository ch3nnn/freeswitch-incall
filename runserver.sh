#!/bin/sh

# shellcheck disable=SC2039
# shellcheck disable=SC2034
# shellcheck disable=SC2112
# shellcheck disable=SC2009
# shellcheck disable=SC2126
# shellcheck disable=SC2004


# Author: ChenTong
# Date: 2022/01/05 16:10

AppName=InCallApplication.py



# 检测 python 版本
PY_VERSION=$(python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}')

if (( $PY_VERSION == 2 ))
then
   python=python3
elif (( $PY_VERSION == 3 ))
then
   python=python
fi

# 判断操作
if [ "$1" = "" ];
then
    echo -e "\033[0;31m 未输入操作名 \033[0m  \033[0;34m {start|stop|restart|status} \033[0m"
    exit 1
fi

# 运行
function start()
{
    PID=$(ps -ef |grep $python|grep $AppName|grep -v grep|awk '{print $2}')

	if [ x"$PID" != x"" ]; then
	    echo "$AppName is running..."
	else
		nohup $python $AppName > /dev/null 2>&1 &
		echo "Start $AppName success..."
	fi
}

# 停止
function stop()
{
    echo "Stop $AppName"

	PID=""
	query(){
		PID=$(ps -ef |grep $python|grep $AppName|grep -v grep|awk '{print $2}')
	}

	query
	if [ x"$PID" != x"" ]; then
		kill -TERM "$PID"
		echo "$AppName (pid:$PID) exiting..."
		while [ x"$PID" != x"" ]
		do
			sleep 1
			query
		done
		echo "$AppName exited."
	else
		echo "$AppName already stopped."
	fi
}

# 重启
function restart()
{
    stop
    sleep 2
    start
}

# 状态
function status()
{
    PID=$(ps -ef |grep $python|grep $AppName|grep -v grep|wc -l)
    if [ $PID != 0 ];then
        echo "$AppName is running..."
    else
        echo "$AppName is not running..."
    fi
}

case $1 in
    start)
    start;;
    stop)
    stop;;
    restart)
    restart;;
    status)
    status;;
    *)
    echo -e "\033[0;31m 输入操作名错误 \033[0m  \033[0;34m {start|stop|restart|status} \033[0m"
esac
