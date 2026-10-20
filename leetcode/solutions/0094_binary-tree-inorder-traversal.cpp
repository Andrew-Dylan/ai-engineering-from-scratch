// 94. Binary Tree Inorder Traversal — 调试学习版
// 用法：
//   1. Cmd+Shift+B  运行 → 看"带日志"输出，直观看到递归调用过程
//   2. F5 断点调试  在 main() 里 sol.inorderTraversal(root) 那行设断点，
//      F11 步入 → 看 dfs() 是怎么一步步执行、一层层递归的
// 提交 LeetCode 时只需复制 Solution 类（TreeNode 和 main 都不需要）。
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

// ============ 标准递归解法（LeetCode 提交用这个） ============
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        dfs(root, res);
        return res;
    }

private:
    void dfs(TreeNode* node, vector<int>& res) {
        if (!node) return;          // 空节点：结束
        dfs(node->left, res);       // 步骤1：去左子树
        res.push_back(node->val);   // 步骤2：访问自己（断点设在这行）
        dfs(node->right, res);      // 步骤3：去右子树
    }
};

// ============ 带日志版本：自动打印每一步，模拟"逐步执行" ============
void dfsDebug(TreeNode* node, vector<int>& res, int depth) {
    string indent(depth * 2, ' ');
    if (!node) {
        cout << indent << "· 遇到空节点 → 直接返回\n";
        return;
    }
    cout << indent << "→ 进入节点 " << node->val << "（递归第 " << depth << " 层）\n";
    cout << indent << "   ① 去左子树：\n";
    dfsDebug(node->left, res, depth + 1);
    cout << indent << "   ② 访问自己 → 输出 " << node->val << "\n";
    res.push_back(node->val);
    cout << indent << "   ③ 去右子树：\n";
    dfsDebug(node->right, res, depth + 1);
    cout << indent << "← 节点 " << node->val << " 处理完毕，返回上一层\n";
}

int main() {
    // 测试树:     1
    //              \
    //               2
    //              /
    //             3
    // 期望中序: 1 3 2
    TreeNode* root = new TreeNode(1, nullptr, new TreeNode(2, new TreeNode(3), nullptr));

    cout << "========== 带日志运行（看看递归怎么执行的）==========\n\n";
    vector<int> res;
    dfsDebug(root, res, 0);

    cout << "\n========== 最终结果 ==========\n中序遍历: ";
    for (int x : res) cout << x << " ";
    cout << "\n\n";

    // 标准解法跑一遍，确认两种输出一致
    Solution sol;
    vector<int> res2 = sol.inorderTraversal(root);
    cout << "标准解法输出: ";
    for (int x : res2) cout << x << " ";
    cout << "\n";

    bool ok = (res == res2 && res2 == (vector<int>{1, 3, 2}));
    cout << (ok ? "\n✅ 结果正确: 1 3 2\n" : "\n❌ 结果不对\n");
    return ok ? 0 : 1;
}
