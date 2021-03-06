from Analysys.pnn import Stalin3000_anal_probe
from tqdm import notebook
import torch
import torch.utils.data as utils_data
import numpy as np
import matplotlib.pyplot as plt
import csv
import pprint
from math import *
BS = 4


class NumDs(utils_data.Dataset):
    def __init__(self, inp, outp):
        self.data = list(zip(inp,outp))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        fea, target = self.data[index]

        return fea, target


class CommunistNN:

    def __init__(self, input_data=None, outputdata=None, mode="train"):

        self.pnn = Stalin3000_anal_probe(5)
        if mode == "test" or mode == "next  train":
            self.pnn.load_state_dict(torch.load('./Analysys/pnn_weights'))
            if mode == "test":
                self.pnn.eval()

        if mode != "test":
            trainset = NumDs(input_data[:-len(input_data) // 4], outputdata[:-len(input_data) // 4])
            trainloader = utils_data.DataLoader(trainset, batch_size=BS, shuffle=True, num_workers=2)

            testset = NumDs(input_data[-len(input_data) // 4:], outputdata[-len(input_data) // 4:])
            testloader = utils_data.DataLoader(testset, batch_size=BS, shuffle=False, num_workers=2)
            loss_fn = torch.nn.MSELoss()

            # выбираем алгоритм оптимизации и learning_rate
            learning_rate = 5e-2
            optimizer = torch.optim.Adam(self.pnn.parameters(), lr=learning_rate,weight_decay=5e-3)
            # pprint.pprint(list(self.pnn.parameters()))
            losses = []

            # итерируемся
            for epoch in notebook.tqdm(range(40)):
                self.pnn.train()
                running_loss = 0.0
                for i, batch in enumerate(notebook.tqdm(trainloader)):
                    # так получаем текущий батч
                    X_batch, y_batch = batch

                    # обнуляем веса
                    optimizer.zero_grad()

                    # forward + backward + optimize
                    y_pred = self.pnn(X_batch)
                    # print(y_batch.shape, "\n\n", y_pred.shape)
                    loss = loss_fn(y_pred, y_batch)
                    loss.backward()
                    optimizer.step()

                    # выведем текущий loss
                    running_loss += loss.item()
                    # выведем качество каждые 2000 батчей
                    if i % 20 == 19:
                        print('[%d, %5d] loss: %.3f' %
                              (epoch + 1, i + 1, running_loss / 2000))
                        losses.append(running_loss)
                        running_loss = 0.0

                if epoch%40 == 39:
                    plt.figure(figsize=(10, 7))
                    plt.plot(np.arange(len(losses)), losses)
                    plt.show()

            print('Обучение закончено')

            error = 0
            total = 0
            self.pnn.eval()
            with torch.no_grad():
                for data in testloader:
                    images, labels = data
                    y_pred = self.pnn(images)
                    predicted = y_pred
                    print(y_pred, "\n\n", y_batch, "\n\n\n\n")
                    c = sum([abs(predicted[i]-labels[i]) for i in range(len(labels))])/len(labels)
                    print("\n",c,"\n")
                    for i in range(BS):
                        label = labels[i]
                        error += c
                        total += 1

            print('Error is : %f' % (c/total))

            torch.save(self.pnn.state_dict(), "./pnn_weights")

    def eval_single(self, x):
        with torch.no_grad():
            self.pnn.eval()
            res = self.pnn(torch.Tensor(x).float().unsqueeze(0))
        return res

def calcit(p1,p2=0,p3=0,p4=0,p5=0):
    Stalin_with_probe = CommunistNN(mode="test")
    return float(Stalin_with_probe.eval_single([p1, p2, p3, p4, p5])[0][0])

def train_nn(table, values_predicted):
    CommunistNN(table, values_predicted, mode="next train")

def clast (table, values_predicted):

    def ro(a, b, c, d):  # расстояние
        return sqrt((a - c) * (a - c) + (b - d) * (b - d))

    N = [table[i].insert(0,values_predicted[i]) for i in range(len(values_predicted))]  # потом сюда добавить ввод данных, 1 символ в каждой строчке массива - время, которое продержалась дорога(сейчас тут значения для теста)
    N1 = [[] for _ in range(len(N))]
    s = 0
    for i in range(len(N)):
        N1[i].append(N[i][0])
        for j in range(len(N[0]) - 1):
            s += N[i][j + 1]  # здесь можно вставлять разные хеш функции, я беру просто сложение
        N1[i].append(s)
        s = 0
    print(N1)
    N2 = [[] for _ in range(len(N1))]
    for i in range(len(N1)):
        for j in range(len(N1)):
            N2[i].append(ro(N1[i][0], N1[i][1], N1[j][0], N1[j][1]))
    return N2


if __name__ ==  "__main__":
    mat = list()
    with open('test_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mat.append([float(row['Temperature (K)']),float(row['Luminosity(L/Lo)']),float(row['Radius(R/Ro)']),float(row['Star type']),1,float(row['Absolute magnitude(Mv)'])])
    # pprint.pprint(np.array(mat)[:,-1:])
    # mat = list(zip(list(range(1,1000)),list(range(4000,3001,-1)),list(range(10,10000,10)),list(range(1001,2000)),list(map(lambda x: 0,range(1,1000))),list(map(lambda x: x[0]*x[1]*x[2]*x[3],zip(list(range(1,1000)),list(range(4000,3001,-1)),list(range(10,10000,10)),list(range(1001,2000)),list(map(lambda x: 0,range(1,1000))))))))
    # pprint.pprint(mat)
    Stalin_with_probe = CommunistNN(np.array(mat,dtype="float32")[:,:-1],np.array(mat,dtype="float32")[:,-1:], mode="train")
    pprint.pprint(float(Stalin_with_probe.eval_single([3068, 0.0024, 0.17, 0, 1])[0][0]))
    # pprint.pprint(list(Stalin_with_probe.pnn.parameters()))