### Запуск
~~~
pip install streamlit
streamlit run main.py
~~~

### Ограничения и допущения
1. Не учитывается снижение потока при очереди > 7. В моем понимании (и моей модели классов) поток клиентов не зависит от банка, прокидывать эту связь неудобно.
2. За один шаг моделирования может прийти максимум один клиент.
3. По окончании дня обслуживание завершается моментально, а клиенты из очереди уходят. При перерыве на обед клиенты тоже идут обедать, так что это не считается ожиданием :)
