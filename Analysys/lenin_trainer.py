from Analysys.pnn import Stalin3000_anal_probe
from tqdm import notebook
import torch
import torch.utils.data as utils_data
import numpy as np
import matplotlib.pyplot as plt
import csv
import pprint


class NumDs(utils_data.Dataset):
    def __init__(self, inp, outp):
        self.data = list(zip(inp,outp))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        fea, target = self.data[index]

        return fea, target


class CommunistNN:

    def __init__(self, input_data, outputdata):

        trainset = NumDs(input_data[:-len(input_data)//4], outputdata[:-len(input_data)//4])
        trainloader = utils_data.DataLoader(trainset, batch_size=1, shuffle=True, num_workers=2)

        testset = NumDs(input_data[-len(input_data)//4:], outputdata[-len(input_data)//4:])
        testloader = utils_data.DataLoader(testset, batch_size=1, shuffle=False, num_workers=2)

        pnn = Stalin3000_anal_probe(5)
        loss_fn = torch.nn.CrossEntropyLoss()

        # выбираем алгоритм оптимизации и learning_rate
        learning_rate = 1e-4
        optimizer = torch.optim.Adam(pnn.parameters(), lr=learning_rate)
        losses = []

        # итерируемся
        for epoch in notebook.tqdm(range(20)):
            pnn.train()
            running_loss = 0.0
            for i, batch in enumerate(notebook.tqdm(trainloader)):
                # так получаем текущий батч
                X_batch, y_batch = batch

                # обнуляем веса
                optimizer.zero_grad()

                # forward + backward + optimize
                y_pred = pnn(X_batch.float())
                # print(y_batch, "\n\n", y_pred)
                loss = loss_fn(y_pred, y_batch)
                loss.backward()
                optimizer.step()

                # выведем текущий loss
                running_loss += loss.item()
                # выведем качество каждые 2000 батчей
                if i % 200 == 199:
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    losses.append(running_loss)
                    running_loss = 0.0

            plt.figure(figsize=(10, 7))
            plt.plot(np.arange(len(losses)), losses)
            plt.show()

        print('Обучение закончено')

        error = 0
        total = 0
        pnn.eval()
        with torch.no_grad():
            for data in testloader:
                images, labels = data
                y_pred = pnn(images)
                _, predicted = torch.max(y_pred, 1)

                c = sum([abs(predicted[i]-labels[i]) for i in range(len(labels))])/len(labels)
                for i in range(1):
                    label = labels[i]
                    error += c
                    total += 1

        for i in range(10):
            print('Error is : %f %%' % (c/total))

        torch.save(pnn.state_dict(), "./pnn_weights")

if __name__ ==  "__main__":
    mat = list()
    with open('test_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mat.append([float(row['Temperature (K)']),float(row['Luminosity(L/Lo)']),float(row['Radius(R/Ro)']),float(row['Star type']),0,float(row['Absolute magnitude(Mv)'])])
    # pprint.pprint(np.array(mat)[:,-1:])
    CommunistNN(np.array(mat,dtype=float)[:,:-1],np.array(mat,dtype=float)[:,-1:])