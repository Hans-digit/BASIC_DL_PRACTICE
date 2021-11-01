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
import loguru

device = ('cuda' if torch.cuda.is_available() else 'cpu')
print(f'device : {device}')
LOGGER = loguru.logger

def ans_to_onehot(ans_tensor, gomoku_dim):
    result = torch.zeros((ans_tensor.size()[0], gomoku_dim * gomoku_dim))
    result[range(ans_tensor.size()[0]), ans_tensor] = 1
    return result


def train(batch_size, train_size, model):
    referee = Referee()
    gomoku = Gomoku()
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()
    weight_tensor = torch.FloatTensor([2, -3]).to(device)
    # # scheduler = optim.lr_scheduler.LambdaLR(optimizer = optimizer, lr_lambda = lambda epoch:0.95 **epoch, last_epoch = -1)
    # scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=3, eta_min=0.001)


    for _ in tqdm(range(train_size)):
        time.sleep(1)
        print(f'train step {_}')

        black_tensor = torch.empty(0, 12, 15, 15).to(device)
        white_tensor = torch.empty(0, 12, 15, 15).to(device)

        black_list_ans = torch.empty(0, 1).to(device)
        white_list_ans = torch.empty(0, 1).to(device)

        # model eval mode
        model.eval()
        for batch in tqdm(range(batch_size)):
            # initial start
            # get train data part
            black_tensor_temp = torch.empty(0, 12, 15, 15).to(device)
            white_tensor_temp = torch.empty(0, 12, 15, 15).to(device)

            black_list_point = []
            white_list_point = []

            # white_first_move_history = []
            # white_first_move_value_list = []
            # white_first_move_count_list = []
            # white_move_history = []

            for i in range(gomoku.gomoku_dim * gomoku.gomoku_dim):
                if i%2 == 0:
                    # black_first_move_history = []
                    # black_first_move_value_list = []
                    # black_first_move_count_list = []

                    move_history = []
                    # black_move_history = []
                    # white_move_history = []
                    # black_move_value = []
                    # black_move_count = []

                    mcts_index = 0

                    while mcts_index < 1600:
                        result, first_move_black = gomoku.get_first_move(black_list_point, white_list_point, move_history)
                        if result == 'reached':
                            #all move data in list, considering sequence
                            #this should be in list
                            #total
                            move_list = []
                            #black
                            move_black_list = []
                            #white
                            move_white_list = []

                            #move data of black in set, not considering sequence
                            #this should be in integer
                            move_black_set = set()
                            move_white_set = set()


                            move_list.append(first_move_black)
                            move_black_list.append(first_move_black)
                            move_black_set.add(first_move_black[0]*15 + first_move_black[1])
                            while True:
                                point_situ = gomoku.get_gomoku_to_tensor(black_list_point + move_black_list, white_list_point + move_white_list)
                                move_possibilities, state_value = model(point_situ)[:-1].tolist(), model(point_situ)[-1].item()
                                nth_move_white = gomoku.get_nth_move(black_list_point + move_black_list, white_list_point + move_white_list,
                                                                     move_history, move_possibilities, target_stone_color = 'black')
                                move_list.append(nth_move_white)
                                move_white_list.append(nth_move_white)
                                move_white_set.add(nth_move_white)

                                check_flag = 0
                                for history_index in move_history:
                                    if move_black_set == history_index[0]:
                                        if move_white_set == history_index[1]:
                                            check_flag = 1
                                            break

                                # when its totally new point
                                if check_flag == 0:
                                    move_history.append([move_black_set, move_white_set, 1, state_value])
                                    move_history = gomoku.update_state_value(move_history, move_list, state_value, start_stone_color='black')
                                    mcts_index += 1
                                    break

                                # when its already used point
                                else:
                                    point_situ = gomoku.get_gomoku_to_tensor(black_list_point + move_black_list, white_list_point + move_white_list)
                                    move_possibilities, state_value = model(point_situ)[:-1].tolist(), model(point_situ)[-1].item()
                                    nth_move_white = gomoku.get_nth_move(black_list_point + move_black_list, white_list_point + move_white_list, move_history, move_possibilities, target_stone_color = 'white')
                                    move_list.append(nth_move_white)
                                    move_white_list.append(nth_move_white)
                                    move_white_set.add(nth_move_white)

                                    check_flag = 0
                                    for history_index in move_history:
                                        if move_black_set == history_index[0]:
                                            if move_white_set == history_index[1]:
                                                check_flag = 1
                                                break

                                    if check_flag == 0:
                                        move_history.append([move_black_set, move_white_set, 1, state_value])
                                        move_history = gomoku.update_state_value(move_history, move_list, state_value,start_stone_color='black')
                                        mcts_index += 1
                                        break

                                    else:
                                        pass
                        else:
                            black_first_move_history.append(first_move_black)
                            black_point_situ = gomoku.get_gomoku_to_tensor(black_list_point + first_move_black, white_list_point).to(device)
                            black_first_move_value = model(black_point_situ)[-1].item()
                            black_first_move_count_list.append(1)
                            black_first_move_value_list.append(black_first_move_value)

                            mcts_index += 1





                    # test possible situations
                    black_point_value = model(black_point_situ).to(device)
                    black_point_value = black_point_value.matmul(weight_tensor)
                    black_point_max = torch.argmax(black_point_value, dim=0)
                    black_point_max = black_point_max.item()

                    target_point = possible_states[black_point_max]
                    black_point = black_point_possible_situ[black_point_max, :, :, :].unsqueeze(dim=0)


                    if referee.check_3_count(target_point, black_list_point, white_list_point):
                        target_index = 1
                        target_point_top10 = black_point_value.topk(black_point_value.size()[0]).indices
                        while target_index < 200:
                            target_point_int = target_point_top10[target_index].item()
                            target_point = possible_states[target_point_int]
                            if referee.check_3_count(target_point, black_list_point, white_list_point):
                                target_index += 1
                            else:
                                black_list_point.append(target_point)
                                black_tensor_temp = torch.cat((black_tensor_temp, black_point_possible_situ[target_point_int, :, :, :].unsqueeze(dim=0)), dim=0)
                                # black_list_temp_ans = torch.cat((black_list_temp_ans, target_point), dim=0)
                                break
                        if target_index == 200:
                            break
                    else:
                        black_list_point.append(target_point)
                        black_tensor_temp = torch.cat((black_tensor_temp, black_point), dim=0)
                        # black_list_temp_ans = torch.cat((black_list_temp_ans, black_point), dim=0)

                    if referee.end_check(black_list_point):
                        black_list_temp_ans = torch.FloatTensor([[0] for i in range(black_tensor_temp.size()[0])]).to(device)
                        white_list_temp_ans = torch.FloatTensor([[1] for i in range(white_tensor_temp.size()[0])]).to(device)
                        black_tensor = torch.cat((black_tensor, black_tensor_temp), dim = 0)
                        black_list_ans = torch.cat((black_list_ans, black_list_temp_ans), dim = 0)
                        white_tensor = torch.cat((white_tensor, white_tensor_temp), dim=0)
                        white_list_ans = torch.cat((white_list_ans, white_list_temp_ans), dim=0)
                        break

                else:
                    # if gomoku.random_put(random_probability):
                    #     white_point = gomoku.random_point(white_list_point, black_list_point)
                    #     white_list_point.append(white_point)
                    # else:
                    # now situation
                    white_point_situ = gomoku.get_gomoku_to_tensor(white_list_point, black_list_point).to(device)

                    # possible situations
                    white_point_possible_situ, possible_states = gomoku.gomoku_possibilities_to_tensor(white_list_point, black_list_point)
                    white_point_possible_situ = white_point_possible_situ.to(device)

                    # test possible situations
                    white_point_value = model(white_point_possible_situ, white_point_possible_situ.size()[0]).to(device)
                    white_point_value = white_point_value.matmul(weight_tensor)
                    white_point_max = torch.argmax(white_point_value, dim=0)
                    white_point_max = white_point_max.item()

                    target_point = possible_states[white_point_max]
                    black_point = white_point_possible_situ[white_point_max, :, :, :].unsqueeze(dim=0)

                    if referee.check_3_count(target_point, white_list_point, black_list_point):
                        target_index = 1
                        target_point_top10 = white_point_value.topk(white_point_value.size()[0]).indices
                        while target_index < 200:
                            target_point_int = target_point_top10[target_index].item()
                            target_point = possible_states[target_point_int]
                            if referee.check_3_count(target_point, white_list_point, black_list_point):
                                target_index += 1
                            else:
                                white_list_point.append(target_point)
                                # target_point = target_point_top10[target_index].view(1, 1)
                                white_tensor_temp = torch.cat((white_tensor_temp, white_point_possible_situ[target_point_int, :, :, :].unsqueeze(dim=0)), dim=0)
                                # white_list_temp_ans = torch.cat((white_list_temp_ans, target_point), dim=0)
                                break
                        if target_index == 200:
                            break
                    else:
                        white_list_point.append(target_point)
                        white_tensor_temp = torch.cat((white_tensor_temp, white_point_situ), dim=0)
                        # white_list_temp_ans = torch.cat((white_list_temp_ans, white_point), dim=0)

                    if referee.end_check(white_list_point):
                        black_list_temp_ans = torch.FloatTensor([[1] for i in range(black_tensor_temp.size()[0])]).to(device)
                        white_list_temp_ans = torch.FloatTensor([[0] for i in range(white_tensor_temp.size()[0])]).to(device)
                        black_tensor = torch.cat((black_tensor, black_tensor_temp), dim=0)
                        black_list_ans = torch.cat((black_list_ans, black_list_temp_ans), dim=0)
                        white_tensor = torch.cat((white_tensor, white_tensor_temp), dim=0)
                        white_list_ans = torch.cat((white_list_ans, white_list_temp_ans), dim=0)
                        break


        # model train mode

        model.train()
        batch_size_train = 30
        black_list_ans = black_list_ans.squeeze()
        black_list_ans = black_list_ans.type(torch.LongTensor)
        white_list_ans = white_list_ans.squeeze()
        white_list_ans = white_list_ans.type(torch.LongTensor)

        total_tensor_situ = torch.cat((black_tensor, white_tensor), dim = 0).to(device)
        total_ans = torch.cat((black_list_ans, white_list_ans), dim = 0).to(device)

        ds = TensorDataset(total_tensor_situ, total_ans)
        try:
            loader = DataLoader(ds, batch_size = batch_size_train, drop_last = True, shuffle = True)

            for epoch in range(5):
                for x_situ, y_ans in loader:
                    try:
                        optimizer.zero_grad()
                        y_pred = model(x_situ, batch_size_train).to(device)
                        print(y_pred)
                        print(y_ans)
                        loss = criterion(y_pred, y_ans)
                        loss.backward()
                        optimizer.step()
                    except Exception as e:
                        print(e)

        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(f'ds is {ds}')




    torch.save(model.state_dict(), 'model/model_CNN2.bin')


def main(args):
    if args.iter is None:
        print('put iter ( -i ) argument')
        return ''


    if args.type == 'fine':
        model = CNN_Gomoku().to(device)
        model.load_state_dict(torch.load('./model/model_CNN2.bin'))
        train(5, int(args.iter), model)
    elif args.type == 'init':
        model = CNN_Gomoku().to(device)
        train(5, int(args.iter), model)
        pass
    else:
        print('put correct type (-t) argument')
        return ''


if __name__== '__main__':
    parser = argparse.ArgumentParser(description='us market analyst report tiprank')
    parser.add_argument('-t', '--type', required=True, help='set train type | fine : fine-tuning task, init : initial learning task')
    parser.add_argument('-i', '--iter', required=True, help='set train number | basic train batch number : 100, you should put train iter number')
    loguru.logger.add('./log/GOMOKU.log',
                      rotation='10MB', retention=5,
                      level='INFO', encoding="utf8")

    args = parser.parse_args()
    main(args)
    # batch size, train size