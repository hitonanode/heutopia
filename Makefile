.PHONY: build format pyformat run train show-studies clean

build: main.cpp
	g++-14 -Wfatal-errors -Wall -Wextra -g -O2 -std=c++20 -DHITONANODE_LOCAL -DBENCHMARK main.cpp -o solver.out

format:
	find ./ -name "*.hpp" -o -name "*.cpp" | xargs clang-format --Werror -i -style=file

pyformat:
	poetry run ruff format .
	poetry run ruff check . --fix
	poetry run mypy .

run:
	poetry run python -m heutopia.run

train:
	poetry run python -m heutopia.train

show-studies:
	poetry run optuna studies  --storage sqlite:///train.db

clean:
	${RM} solver.out
