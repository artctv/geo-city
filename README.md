# geo-city
Multiprocessing calculation distance betwen cities


## Задача

Скрипт на python, который принимает на входе список всех населенных пунктов страны с координатами 
(~150 000 городов) и выдает за разумное время следующий результат:
 - расстояния по дуге геоида между каждой парой городов - в виде матрицы в CSV


## Запуск

- Установить зависимости
- Перейти в дирректорию `geo-city/harvesine`
- Скомпилировать C-extension:
    ```bash
    python3 setup.py build_ext --inplace
    ```
- Вернуться в корень
- Выполнить: 
  ```bash
    python3 geo-city/main.py
  ```