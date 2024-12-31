#!/bin/sh
if [ -e "/work/app/ptb_dump.bin" ]
then
	echo "file already exists -> /work/app/ptb_dump.bin"
else
	echo "Nanddump PTB -> /work/app/ptb_dump.bin"
	nanddump -f /work/app/ptb_dump.bin /dev/mtd2
	sync
fi

