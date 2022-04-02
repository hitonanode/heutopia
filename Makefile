solver.out: main.cpp
	g++-11 -Wfatal-errors -Wall -Wextra -g -O2 -fsanitize=undefined -std=c++17 -DHITONANODE_LOCAL -DBENCHMARK -fsplit-stack main.cpp -o solver.out
