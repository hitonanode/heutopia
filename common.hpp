#pragma once
#include <iostream>

#include "json_dumper.hpp"

#ifdef BENCHMARK
#define dump_onlinejudge(x) 0
struct setenv {
  setenv() { jdump.set_dump_at_end(); }
} setenv_;
#else
#define dump_onlinejudge(x) (std::cout << (x) << std::endl)
#endif
