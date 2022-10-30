solver.out: main.cpp
	g++-11 -Wfatal-errors -Wall -Wextra -g -O2 -fsanitize=undefined -std=c++17 -DHITONANODE_LOCAL -DBENCHMARK -fsplit-stack main.cpp -o solver.out

format:
	poetry run black .
	poetry run flake8 .
	poetry run mypy .

run:
	poetry run python run.py

train:
	poetry run python train.py

clean:
	${RM} solver.out
