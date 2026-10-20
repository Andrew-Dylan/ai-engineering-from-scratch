#include <iostream>
#include <vector>
using namespace std;


class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size();
        if (m == 0) return;
        int n = matrix[0].size();
        bool rowzero = false, colzero = false;
        for(int i = 0; i < m; i++){
            for(int j = 0; j < n; j++){
                if(matrix[i][j] == 0){
                    if(i == 0) rowzero = true;
                    if(j == 0) colzero = true;
                    matrix[i][0] = 0;
                    matrix[0][j] = 0;
                }
            }
        }
        for(int i = 1; i < m; i++){
            for(int j = 1; j < n; j++){
                if(matrix[i][0] == 0 || matrix[0][j] == 0){
                    matrix[i][j] = 0;
                }
            }
        }
        if(rowzero){
            for(int j = 0; j < n; j++){
                matrix[0][j] = 0;
            }
        }
        if(colzero){
            for(int i = 0; i < m; i++){
                matrix[i][0] = 0;
            }
        }
    }
};

int main() {
    Solution sol;

    struct Case {
        vector<vector<int>> input;
        vector<vector<int>> expected;
    };
    vector<Case> cases = {
        {{{1, 1, 1}, {1, 0, 1}, {1, 1, 1}}, {{1, 0, 1}, {0, 0, 0}, {1, 0, 1}}},
        {{{0, 1, 2, 0}, {3, 4, 5, 2}, {1, 3, 1, 5}}, {{0, 0, 0, 0}, {0, 4, 5, 0}, {0, 3, 1, 0}}},
        {{{1, 0, 1}}, {{0, 0, 0}}},                 // 单行
        {{{1}, {0}, {1}}, {{0}, {0}, {0}}},         // 单列
        {{{1, 2}, {3, 4}}, {{1, 2}, {3, 4}}},       // 无零
        {{{0}}, {{0}}},                             // 单元素为 0
    };

    int passed = 0;
    for (size_t i = 0; i < cases.size(); ++i) {
        auto got = cases[i].input;
        sol.setZeroes(got);
        bool ok = got == cases[i].expected;
        passed += ok;
        cout << "case " << i << ": " << (ok ? "PASS" : "FAIL");
        if (!ok) {
            cout << "  got:";
            for (auto& row : got) {
                cout << " [";
                for (int x : row) cout << x << " ";
                cout << "]";
            }
        }
        cout << "\n";
    }
    cout << passed << "/" << cases.size() << " passed\n";
    return passed == static_cast<int>(cases.size()) ? 0 : 1;
}