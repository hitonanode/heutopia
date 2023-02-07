#include "common.hpp"

using namespace std;
using lint = long long;
using pint = pair<int, int>;
using plint = pair<lint, lint>;

struct fast_ios {
    fast_ios() { cin.tie(nullptr), ios::sync_with_stdio(false), cout << fixed << setprecision(20); };
} fast_ios_;

int main(int argc, char *argv[]) {
    int X = 0;
    if (argc >= 2) { X = std::stoi(argv[1]); }

    int x;
    cin >> x;
    jdump("stdin", x);

    dump_onlinejudge("solution"s);

    jdump("score", -(X - 6) * (X - 6));
}
