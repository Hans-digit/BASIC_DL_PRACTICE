from referee import Referee
from gomoku import Gomoku
from model import CNN_Gomoku
import math
import torch
import time
import random
from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm
import argparse

device = ('cuda' if torch.cuda.is_available() else 'cpu')
print(f'device : {device}')


def ans_to_onehot(ans_tensor, gomoku_dim):
    result = torch.zeros((ans_tensor.size()[0], gomoku_dim * gomoku_dim))
    result[range(ans_tensor.size()[0]), ans_tensor] = 1
    return result


def train(batch_size, train_size, model):
    print('train start')
    random_probability = 0.1
    referee = Referee()
    gomoku = Gomoku()
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()
    # # scheduler = optim.lr_scheduler.LambdaLR(optimizer = optimizer, lr_lambda = lambda epoch:0.95 **epoch, last_epoch = -1)
    # scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=3, eta_min=0.001)


    for _ in tqdm(range(train_size)):
        print(f'train step {_}')

        black_tensor = torch.empty(0, 12, 15, 15).to(device)
        white_tensor = torch.empty(0, 12, 15, 15).to(device)

        black_list_ans = torch.empty(0, 1).to(device)
        white_list_ans = torch.empty(0, 1).to(device)

        # model eval mode
        model.eval()
        for batch in range(batch_size):
            # initial start
            # get train data part
            black_tensor_temp = torch.empty(0, 12, 15, 15).to(device)
            white_tensor_temp = torch.empty(0, 12, 15, 15).to(device)
            black_list_temp_ans = torch.empty(0, 1).to(device)
            white_list_temp_ans = torch.empty(0, 1).to(device)

            black_list_point = []
            white_list_point = []

            for i in range(gomoku.gomoku_dim * gomoku.gomoku_dim):
                if i%2 == 0:
                    if gomoku.random_put(random_probability):
                        black_point = gomoku.random_point(black_list_point, white_list_point)
                        black_list_point.append(black_point)
                    else:
                        black_point_situ = gomoku.gomoku_to_tensor(black_list_point, white_list_point).to(device)
                        black_point = model(black_point_situ, 1).to(device)
                        black_point = torch.argmax(black_point, dim=1)
                        black_point_int = black_point.item()
                        black_point = black_point.view(1,1)
                        quotient, remainder = math.floor(black_point_int / 15), black_point_int % 15
                        target_point = [quotient, remainder]

                        if referee.check_3_count(target_point, black_list_point, white_list_point):
                            target_index = 1
                            target_point_top10 = model.get_top10(black_point_situ).indices[0]
                            while target_index < 200:
                                target_point = target_point_top10[target_index].item()
                                quotient, remainder = math.floor(target_point / 15), target_point % 15
                                target_point = [quotient, remainder]
                                if referee.check_3_count(target_point, black_list_point, white_list_point):
                                    target_index += 1
                                else:
                                    black_list_point.append(target_point)
                                    target_point = target_point_top10[target_index].view(1, 1)
                                    black_tensor_temp = torch.cat((black_tensor_temp, black_point_situ), dim=0)
                                    black_list_temp_ans = torch.cat((black_list_temp_ans, target_point), dim=0)
                                    break
                            if target_index == 200:
                                break
                        else:
                            black_list_point.append(target_point)
                            black_tensor_temp = torch.cat((black_tensor_temp, black_point_situ), dim=0)
                            black_list_temp_ans = torch.cat((black_list_temp_ans, black_point), dim=0)

                    if referee.end_check(black_list_point):
                        black_tensor = torch.cat((black_tensor, black_tensor_temp), dim = 0)
                        black_list_ans = torch.cat((black_list_ans, black_list_temp_ans), dim = 0)
                        break

                else:
                    if gomoku.random_put(random_probability):
                        white_point = gomoku.random_point(white_list_point, black_list_point)
                        white_list_point.append(white_point)
                    else:
                        white_point_situ = gomoku.gomoku_to_tensor(white_list_point, black_list_point).to(device)
                        white_point = model(white_point_situ, 1).to(device)
                        white_point = torch.argmax(white_point, dim=1)
                        white_point_int = white_point.item()
                        white_point = white_point.view(1,1)
                        quotient, remainder = math.floor(white_point_int / 15), white_point_int % 15
                        target_point = [quotient, remainder]

                        if referee.check_3_count(target_point, white_list_point, black_list_point):
                            target_index = 1
                            target_point_top10 = model.get_top10(white_point_situ).indices[0]
                            while target_index < 200:
                                target_point = target_point_top10[target_index].item()
                                quotient, remainder = math.floor(target_point / 15), target_point % 15
                                target_point = [quotient, remainder]
                                if referee.check_3_count(target_point, white_list_point, black_list_point):
                                    target_index += 1
                                else:
                                    white_list_point.append(target_point)
                                    target_point = target_point_top10[target_index].view(1, 1)
                                    white_tensor_temp = torch.cat((white_tensor_temp, white_point_situ), dim=0)
                                    white_list_temp_ans = torch.cat((white_list_temp_ans, target_point), dim=0)
                                    break
                            if target_index == 200:
                                break
                        else:
                            white_list_point.append(target_point)
                            white_tensor_temp = torch.cat((white_tensor_temp, white_point_situ), dim=0)
                            white_list_temp_ans = torch.cat((white_list_temp_ans, white_point), dim=0)

                    if referee.end_check(white_list_point):
                        white_tensor = torch.cat((white_tensor, white_tensor_temp), dim=0)
                        white_list_ans = torch.cat((white_list_ans, white_list_temp_ans), dim=0)
                        break


        # model train mode

        model.train()
        batch_size = 30
        black_list_ans = black_list_ans.squeeze()
        black_list_ans = black_list_ans.type(torch.LongTensor)
        white_list_ans = white_list_ans.squeeze()
        white_list_ans = white_list_ans.type(torch.LongTensor)

        total_tensor_situ = torch.cat((black_tensor, white_tensor), dim = 0).to(device)
        total_ans = torch.cat((black_list_ans, white_list_ans), dim = 0).to(device)

        ds = TensorDataset(total_tensor_situ, total_ans)
        loader = DataLoader(ds, batch_size = batch_size, drop_last = True, shuffle = True)

        for epoch in range(5):
            for x_situ, y_ans in loader:
                optimizer.zero_grad()
                y_pred = model(x_situ, batch_size).to(device)
                loss = criterion(y_pred, y_ans)
                loss.backward()
                optimizer.step()


    torch.save(model.state_dict(), 'model/model_CNN.bin')


def main(args):
    if args.iter is None:
        print('put iter ( -i ) argument')
        return ''


    if args.type == 'fine':
        model = CNN_Gomoku().to(device)
        model.load_state_dict(torch.load('./model/model_CNN.bin'))
        train(100, int(args.iter), model)
    elif args.type == 'init':
        model = CNN_Gomoku().to(device)
        train(100, int(args.iter), model)
        pass
    else:
        print('put correct type (-t) argument')
        return ''


if __name__== '__main__':
    parser = argparse.ArgumentParser(description='us market analyst report tiprank')
    parser.add_argument('-t', '--type', required=True, help='set train type | fine : fine-tuning task, init : initial learning task')
    parser.add_argument('-i', '--iter', required=True, help='set train number | basic train batch number : 100, you should put train iter number')

    args = parser.parse_args()
    main(args)
    # batch size, train size