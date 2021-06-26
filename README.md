# ambulance_crews
Задача "Потребность в бригадах скорой помощи" от ICL в рамках Digital Healthcare DS Hackathon BCG GAMMA.

## Планы / задачи
Кооперируемся, делаем.
- [ ] Анализ данных (**Люба**)
	* общая статистика
	* соотнесение, на какие вызовы какую бригаду (скор./неотлож.) отправляют
	* загруженность по подстанциям (в т.ч. с учётом времени)
	* проч.
- [ ] EDA (**Люба**)
	* стационарность
	* сезонность
	* автокорреляция
- [ ] Корреляция признаков (**Юля**)
	* между собой
	* с таргетом
- [ ] Создание признаков (**Юля**)
	* понижение размерности
	* из сильно коррелирующих
	* из своих соображений / гипотез
	* по профилям поводов
- [x] Парсинг дополнительных данных (**Саша**)
	* статистика по ковиду / гриппу (интерполировать по часам)
	* погода (температура, влажность, давление, магнитные бури, ветер)
	* фазы Луны, ретроградность Меркурия :)
	* праздничные дни
- [ ] Моделирование (**Илья**)
	* множественная регрессия
	* autoML
	* бустинг
	* arima и проч.
	* гаус. процессы
- [ ] Сервис (**Саша**)
	* web на Flask
	* принимает данные, выдаёт прогноз (графики, таблицы)
	* подумать над бизнес-задачей
		* н-р, можно выдавать рекомендации по распределению юнитов: если по прогнозу где-то больше вызовов, а где-то меньше, то перебрасываем бригады туда, где больше в них потребность
		* можно выдавать сравнительную статистику по нагруженности и те же рекомендации по выделяемому числу ресурсов