import torch
import numpy as np
import random
import pygame as pg
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import torch.nn.functional as F
import torch.nn as nn



def activation(x):
    return F.softmax(x, dim=-1)



loss_fn = nn.CrossEntropyLoss()



X, y = load_digits(return_X_y=True)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)



def make_param(shape, scale=1.0):
    t = torch.randn(shape, dtype=torch.float32) * scale
    return nn.Parameter(t)


layer_1 = make_param((64, 32), 0.2)
bias1   = make_param((32,), 0.0)

layer_2 = make_param((32, 10), 0.2)
bias2   = make_param((10,), 0.0)

layers = [(layer_1, bias1), (layer_2, bias2)]

params = [layer_1, bias1, layer_2, bias2]



epochs = 10
lr = 0.1

acc_plot = []
err_plot = []

for ep in range(epochs):

    correct = 0
    total_loss = 0

    for i, x in enumerate(X_train):
        x_tensor = torch.tensor(x, dtype=torch.float32)

        out = x_tensor
        for w, b in layers:
            out = activation(out @ w + b)

        target = torch.tensor([y_train[i]])

        err = loss_fn(out.unsqueeze(0), target)


        err.backward()


        with torch.no_grad():
            for p in params:
                p -= lr * p.grad
                p.grad.zero_()

        total_loss += err.item()
        if torch.argmax(out).item() == y_train[i]:
            correct += 1


    test_correct = 0
    test_loss = 0

    for i, x in enumerate(X_test):
        out = torch.tensor(x, dtype=torch.float32)
        for w, b in layers:
            out = activation(out @ w + b)

        test_loss += loss_fn(out.unsqueeze(0), torch.tensor([y_test[i]])).item()
        if torch.argmax(out).item() == y_test[i]:
            test_correct += 1

    acc = test_correct / len(X_test)
    err_avg = test_loss / len(X_test)

    acc_plot.append(acc)
    err_plot.append(err_avg)

    print(f"[{ep+1}/{epochs}] acc={acc:.3f}, loss={err_avg:.3f}")



plt.figure(figsize=(8,5))
plt.plot(acc_plot, label="Accuracy", linewidth=3)
plt.plot(err_plot, label="Loss", linewidth=2)
plt.grid(alpha=0.3)
plt.legend()
plt.title("Training progress")
plt.show()



pg.init()

N = 100
field_size = 8
w, h = (field_size * 2) * N, field_size * N
screen = pg.display.set_mode((w, h))
clock = pg.time.Clock()

field = np.zeros(field_size * field_size)

font = pg.font.SysFont("Arial", 26, bold=True)


def think():
    inp = torch.tensor(scaler.transform([field * 16]), dtype=torch.float32)
    out = inp[0]
    for w_, b_ in layers:
        out = activation(out @ w_ + b_)

    screen.fill((225, 240, 225))

    # probabilities
    for i in range(10):
        v = float(out[i])
        pg.draw.rect(screen, (140, 150, 255), (w//2 + 40, 40 + i*40, int(v * 250), 30))
        txt = font.render(f"{i}: {v:.3f}", True, (0,0,80))
        screen.blit(txt, (w//2 + 310, 40 + i*40))

    draw()
    pg.display.update()


def draw():
    for y_ in range(field_size):
        for x_ in range(field_size):
            v = field[y_ * field_size + x_]
            c = int(v * 255)
            pg.draw.rect(screen, (c, c, c), (x_ * N, y_ * N, N, N))



screen.fill((230, 240, 230))
draw()
pg.display.update()


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                think()

            if event.key == pg.K_z:
                field[:] = 0
                think()
                draw()

            if event.key == pg.K_x:
                idx = random.choice(range(len(X_test)))
                field[:] = scaler.inverse_transform(X_test)[idx] / 16
                print("True digit:", y_test[idx])
                think()
                draw()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 2:
                x, y = pg.mouse.get_pos()
                x //= N
                y //= N
                if 0 <= x < field_size and 0 <= y < field_size:
                    field[y * field_size + x] = 0.5

    L = pg.mouse.get_pressed()

    if L[0]:
        x, y = pg.mouse.get_pos()
        x //= N
        y //= N
        idx = y * field_size + x
        if 0 <= idx < len(field):
            field[idx] = min(1, field[idx] + 0.18)
        think()
        draw()

    if L[2]:
        x, y = pg.mouse.get_pos()
        x //= N
        y //= N
        idx = y * field_size + x
        if 0 <= idx < len(field):
            field[idx] = max(0, field[idx] - 0.18)
        think()
        draw()

    pg.display.update()
    clock.tick(60)

pg.quit()
