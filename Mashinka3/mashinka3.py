import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


data = pd.read_csv('C:/Users/User/Downloads/AmesHousing.csv')

target = 'SalePrice'

X = data.drop(columns=[target])
y = data[target]

X = X.select_dtypes(include=[np.number])

X = X.dropna(axis=1)


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


corr_matrix = pd.DataFrame(X_scaled, columns=X.columns).corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]

X_reduced = pd.DataFrame(X_scaled, columns=X.columns).drop(columns=to_drop)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_reduced)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(X_pca[:, 0], X_pca[:, 1], y, c=y, cmap='viridis', alpha=0.7)
ax.set_xlabel('PCA Component 1')
ax.set_ylabel('PCA Component 2')
ax.set_zlabel('SalePrice')
plt.colorbar(sc, label='SalePrice')
plt.title('3D график PCA признаков и SalePrice')
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    X_reduced, y, test_size=0.2, random_state=42
)

alphas = np.logspace(-4, 0, 50)
rmse_list = []

for alpha in alphas:
    model = Lasso(alpha=alpha, max_iter=10000, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    rmse_list.append(rmse)


plt.figure(figsize=(8, 5))
plt.plot(alphas, rmse_list, marker='o')
plt.xscale('log')
plt.xlabel('Коэффициент регуляризации (alpha)')
plt.ylabel('RMSE')
plt.title('Зависимость ошибки RMSE от коэффициента регуляризации Lasso')
plt.grid(True)
plt.show()

best_alpha = alphas[np.argmin(rmse_list)]
print(f"Лучший alpha: {best_alpha}")

best_model = Lasso(alpha=best_alpha, max_iter=10000, random_state=42)
best_model.fit(X_train, y_train)


coef = pd.Series(best_model.coef_, index=X_reduced.columns)
coef_abs = coef.abs()
most_influential_feature = coef_abs.idxmax()
print(f"Признак с наибольшим влиянием на целевое значение: {most_influential_feature}")
print(f"Коэффициент: {coef[most_influential_feature]}")

