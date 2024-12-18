#!/bin/bash
for folder in ElectricDevices #SpokenArabicDigits ArticularyWordRecognition AtrialFibrillation Cricket SelfRegulationSCP1 SelfRegulationSCP2 StandWalkJump
do
  for i in {1..5}
  do
    save_path=exp/$folder/$i
    python main.py \
    --dataset UCR \
    --UCR_folder $folder \
    --data_path data/UCR_UEA/Multivariate_arff/ \
    --device cuda:0 \
    --train_batch_size 64 \
    --test_batch_size 64 \
    --save_path $save_path 
  done
done