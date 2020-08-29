AUTO_SHUTDOWN=1
FINETUNE=1
VERSION=''
MACHINE_NAME=''
ZONE=''
PROJECT=''


if [ $FINETUNE = 1 ]; then
  echo "Start time : "$(date "+%Y-%m-%d %H:%M:%S")
  python3 fine_tune.py \
        --version=$VERSION \
        --tpu=$MACHINE_NAME \
        --model_type='small' \
        --train_data_file='traindata_v2.tsv' \
        --dev_data_file='devdata_v2.tsv' \
        --eval_data_file='testdata_v2.tsv' \
        --epoch=1\
        --prefix='ask_doc:' \
        --batch_size=256
  echo "End time : "$(date "+%Y-%m-%d %H:%M:%S")
fi


if [ $AUTO_SHUTDOWN = 1 ]; then
    echo "Closing $MACHINE_NAME in 0 minutes"
    ctpu pause -name=$MACHINE_NAME -zone=$ZONE -project=$PROJECT -noconf
fi


## nohup bash fine_tune.sh &

