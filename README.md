# ДЗ № 3 "Машинное обучение в продакшене", MADE, весна 2021.

## Деплой Airflow
Запуск Airflow на Ubuntu 20.04:
```docker-compose up --build```  

Запуск интерфейса (необходимо ввести в браузере):
```http://localhost:8080/```  

Завершение работы:
```docker-compose down```  

Тестирование:
```pytest -v```  

## ДАГи:
Реализуйте dag, который генерирует данные для обучения модели (prod3_1_generate_data):
    start (DummyOperator) >> generate_data (DockerOperator) >> end (DummyOperator)

Реализуйте dag, который обучает модель еженедельно, используя данные за текущий день (prod3_2_train_model):
    [data_sensor (FileSensor), target_sensor (FileSensor)] >> build_features (DockerOperator) >> split_data (DockerOperator) >> train_model (DockerOperator) >> validate_model (DockerOperator)

Реализуйте dag, который использует модель ежедневно (prod3_3_predict):
    start (DummyOperator) >> [data_sensor (FileSensor), model_sensor (FileSensor), transformer_sensor (FileSensor) ] >> prediction (DockerOperator) >> end (DummyOperator)

## Самооценка
+ Поднимите airflow локально, используя docker compose 
+ Реализуйте dag, который генерирует данные для обучения модели (5 баллов)
+ Реализуйте dag, который обучает модель еженедельно, используя данные за текущий день. В Вашем пайплайне должно быть как минимум 4 стадии (10 баллов) 
+ Реализуйте dag, который использует модель ежедневно (5 баллов)
+ Реализуйте сенсоры на то, что данные готовы для дагов тренировки и обучения (3 доп. балла)
+ Все даги реализованы только с помощью DockerOperator (10 баллов)
+ Протестируйте Ваши даги (5 баллов) 
+ Настройте alert в случае падения дага (3 доп. балла)
+ Проведите самооценку (1 доп. балл)
+ Итого: 42 * 0.6 = 25 баллов