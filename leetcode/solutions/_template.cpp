// <题号>. <题名> — LeetCode 模板
// 使用方法：
//   1. 复制本文件为 leetcode/solutions/<题号>_<slug>.cpp
//   2. 在 Solution 类中实现题解（保持 LeetCode 站内相同签名）
//   3. 在 main() 中补充测试用例，Cmd+Shift+B 运行，F5 调试
// 注意：类名和函数签名必须与 LeetCode 题目一致，方便粘回提交。
#include <iostream>
#include <vector>

class Solution {
public:
    // 在此实现题解（示例签名，按题目替换）
    int solve(std::vector<int>& nums) {
        int ans = 0;
        for (int x : nums) ans += x;
        return ans;
    }
};

int main() {
    Solution sol;

    struct Case {
        std::vector<int> nums;
        int expected;
    };
    std::vector<Case> cases = {
        {{1, 2, 3}, 6},
        {{}, 0},
    };

    int passed = 0;
    for (size_t i = 0; i < cases.size(); ++i) {
        int got = sol.solve(cases[i].nums);
        bool ok = got == cases[i].expected;
        passed += ok;
        std::cout << "case " << i << ": " << (ok ? "PASS" : "FAIL")
                  << "  got=" << got << " expected=" << cases[i].expected << "\n";
    }
    std::cout << passed << "/" << cases.size() << " passed\n";
    return passed == static_cast<int>(cases.size()) ? 0 : 1;
}
