#!/bin/bash

hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options=-k1,1 \
    -file mapper.py -mapper mapper.py \
    -file reducer_1.py -reducer reducer_1.py \
    -input /user/root/input_data \
    -output /user/root/reducer_1_output_train

hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options=-k1,1 \
    -mapper cat \
    -file reducer_2.py -reducer reducer_2.py \
    -input /user/root/reducer_1_output_train \
    -output /user/root/reducer_2_output_train

