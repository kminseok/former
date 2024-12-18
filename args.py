import argparse
import os
import json
from datautils import load_UCR

parser = argparse.ArgumentParser()
# dataset and dataloader args
parser.add_argument('--dataset', type=str, default='UCR', help='Dataset name') # 추가한 코드
parser.add_argument('--save_path', type=str, default='test')
parser.add_argument('--UCR_folder', type=str, default='ElectricDevices')
parser.add_argument('--data_path', type=str,
                    default='')
parser.add_argument('--device', type=str, default='cuda:0')
parser.add_argument('--train_batch_size', type=int, default=64)
parser.add_argument('--test_batch_size', type=int, default=64)

# model args
parser.add_argument('--dropout', type=float, default=0.2)
parser.add_argument('--attn_heads', type=int, default=4)
parser.add_argument('--eval_per_steps', type=int, default=16)
parser.add_argument('--enable_res_parameter', type=int, default=1)
parser.add_argument('--loss', type=str, default='ce', choices=['bce', 'ce'])
parser.add_argument('--pooling_type', type=str, default='mean', choices=['mean', 'max', 'last_token', 'cat'])
parser.add_argument('--save_model', type=int, default=1)

# FormerTime args
parser.add_argument('--stages', type=int, default=3) # stage 개수
parser.add_argument('--layer_per_stage', type=int, default=[6, 6, 6]) # L_1, L_2, L_3 논문 table2 참조
parser.add_argument('--hidden_size_per_stage', type=list, default=[64, 64, 64]) # C_1, C_2, C_3 논문 table2 참조
parser.add_argument('--slice_per_stage', type=list, default=[2, 2, 2])  # s_1, s_2, s_3 논문 table2 참조
parser.add_argument('--stride_per_stage', type=int, default=[2, 2, 2]) # d_1, d_2, d_3 논문 table2 참조
parser.add_argument('--tr', type=list, default=[2, 2, 1])  # R_1, R_2, R_3 논문 table2 참조
parser.add_argument('--position_location', type=str, default='top', choices=['top', 'middle'])
parser.add_argument('--position_type', type=str, default='static',
                    choices=['cond', 'relative', 'static', 'none', 'conv_static']) # positional Encoding 방법 선택

# train args
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--lr_decay_rate', type=float, default=1.)
parser.add_argument('--lr_decay_steps', type=int, default=100)
parser.add_argument('--weight_decay', type=float, default=0.01)
parser.add_argument('--num_epoch', type=int, default=100)

args = parser.parse_args()
if args.data_path is None:
    Train_data, Test_data = load_UCR(folder=args.UCR_folder)
    args.num_class = len(set(Train_data[1]))
    args.loss = 'ce'
else:
    path = args.data_path
    Train_data, Test_data = load_UCR(path, folder=args.UCR_folder)
    args.num_class = len(set(Train_data[1]))
    args.loss = 'ce'

args.eval_per_steps = max(1, int(len(Train_data[0]) / args.train_batch_size))
args.lr_decay_steps = args.eval_per_steps
if not os.path.exists(args.save_path):
    os.makedirs(args.save_path)
config_file = open(args.save_path + '/args.json', 'w')
tmp = args.__dict__
json.dump(tmp, config_file, indent=1)
print(args)
config_file.close()
