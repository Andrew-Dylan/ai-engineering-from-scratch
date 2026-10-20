// 0001. Two Sum — LeetCode 刷题示例
// 工作流：
//   Cmd+Shift+B   编译并运行（带 ASan/UBSan 内存检测）
//   F5            断点调试（CodeLLDB，自动先编译）
// 新建题目：复制 _template.cpp，或直接参考本文件的结构。
#include <iostream>
#include <unordered_map>
#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> seen;  // value -> index
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            auto it = seen.find(target - nums[i]);
            if (it != seen.end()) {
                return {it->second, i};
            }
            seen[nums[i]] = i;
        }
        return {};  // 题目保证有解，这里仅为编译通过
    }
};

int main() {
    Solution sol;

    struct Case {
        std::vector<int> nums;
        int target;
        std::vector<int> expected;
    };
    std::vector<Case> cases = {
        {{2, 7, 11, 15}, 9, {0, 1}},
        {{3, 2, 4}, 6, {1, 2}},
        {{3, 3}, 6, {0, 1}},
    };

    int passed = 0;
    for (size_t i = 0; i < cases.size(); ++i) {
        auto got = sol.twoSum(cases[i].nums, cases[i].target);
        bool ok = got == cases[i].expected;
        passed += ok;
        std::cout << "case " << i << ": " << (ok ? "PASS" : "FAIL")
                  << "  got=[" << (got.empty() ? -1 : got[0]) << ","
                  << (got.size() > 1 ? got[1] : -1) << "]\n";
    }
    std::cout << passed << "/" << cases.size() << " passed\n";
    return passed == static_cast<int>(cases.size()) ? 0 : 1;
}
