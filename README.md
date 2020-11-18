# flask-app-mipt
Final task

Простое приложение для контроля расходов. Можно добавить потраченную сумму, дату и комментарий. Доступен график, показывающий heatmap за заданный период. Можно сгруппировать расходы по n дней. 

Предупреждение: поскольку это учебный проект, входные данные на корректность не проверялись, поэтому если 

1) в поле сумма указать не число

2) указать неправильно дату, например, 1.10.20 вместо 01.10.2020

3) указать пустой период в анализе

все упадет! 

Как запустить у себя приложение локально (без docker-compose):

1) Запускаем postgres

`cd postgres`

`docker build . -t postgres`

`docker run -p 5432:5432 postgres`

2) Запускаем приложение

`cd web`

`python app.py`

