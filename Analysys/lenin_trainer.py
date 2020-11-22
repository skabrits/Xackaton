from Analysys.pnn import Stalin3000_anal_probe
from tqdm import notebook
import torch
import torch.utils.data as utils_data
import numpy as np
import matplotlib.pyplot as plt
import csv
import pprint
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

    def __init__(self, input_data, outputdata, mode="train"):

        trainset = NumDs(input_data[:-len(input_data)//4], outputdata[:-len(input_data)//4])
        trainloader = utils_data.DataLoader(trainset, batch_size=BS, shuffle=True, num_workers=2)

        testset = NumDs(input_data[-len(input_data)//4:], outputdata[-len(input_data)//4:])
        testloader = utils_data.DataLoader(testset, batch_size=BS, shuffle=False, num_workers=2)

        self.pnn = Stalin3000_anal_probe(5)
        if mode == "test" or mode == "next  train":
            self.pnn.load_state_dict(torch.load('pnn_weights'))
            if mode == "test":
                self.pnn.eval()

        if  mode != "test":
            loss_fn = torch.nn.MSELoss()

            # выбираем алгоритм оптимизации и learning_rate
            learning_rate = 1e-3
            optimizer = torch.optim.Adam(self.pnn.parameters(), lr=learning_rate,weight_decay=5e-4)
            # pprint.pprint(list(self.pnn.parameters()))
            losses = []

            # итерируемся
            for epoch in notebook.tqdm(range(50)):
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
    pprint.pprint(Stalin_with_probe.eval_single([3068, 0.0024, 0.17, 0, 1]))
    # pprint.pprint(list(Stalin_with_probe.pnn.parameters()))