# 94. 二叉树的中序遍历 (Binary Tree Inorder Traversal)

> 给定一个二叉树的根节点 `root`，返回它的 **中序** 遍历。

**难度：** 简单
**标签：** 栈 / 树 / 深度优先搜索 / 二叉树
**LeetCode：** <https://leetcode.cn/problems/binary-tree-inorder-traversal/>

---

## 思路

中序遍历的顺序是 **左子树 → 根节点 → 右子树**。三种写法对应三种典型实现：

| 方法 | 核心思想 | 时间复杂度 | 空间复杂度 |
|------|---------|-----------|-----------|
| 递归 | 函数调用栈天然符合遍历顺序 | O(n) | O(h)，最坏 O(n) |
| 迭代 + 显式栈 | 用 `stack` 模拟递归栈 | O(n) | O(h)，最坏 O(n) |
| Morris | 利用叶子节点的空指针做线索，无额外栈 | O(n) | **O(1)** |

> 题目 Follow-up：递归解法很简单，你能用 **迭代** 完成吗？（对应方法二）

---

## 前置：树节点定义

LeetCode 平台已内置，本地测试时需要自己写：

```cpp
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};
```

---

## 方法一：递归（最直观）

```cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        dfs(root, res);
        return res;
    }

private:
    void dfs(TreeNode* node, vector<int>& res) {
        if (!node) return;
        dfs(node->left, res);   // 左
        res.push_back(node->val); // 根
        dfs(node->right, res);  // 右
    }
};
```

- 时间复杂度：O(n)，每个节点恰好访问一次
- 空间复杂度：O(h)，h 为树高，递归栈最深为树高（最坏退化为链表时 O(n)）

---

## 方法二：迭代 + 显式栈（Follow-up 要求）

模拟递归：一路向左压栈，弹出时访问，再转向右子树。

```cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        stack<TreeNode*> stk;
        TreeNode* cur = root;

        while (cur || !stk.empty()) {
            while (cur) {            // 1. 一路向左，压入左子树路径
                stk.push(cur);
                cur = cur->left;
            }
            cur = stk.top();         // 2. 弹出栈顶 = 最左节点
            stk.pop();
            res.push_back(cur->val); // 3. 访问根
            cur = cur->right;        // 4. 转向右子树（右子树继续同样的循环）
        }
        return res;
    }
};
```

- 时间复杂度：O(n)
- 空间复杂度：O(h)，最坏 O(n)

---

## 方法三：Morris 遍历（O(1) 空间，进阶）

利用叶子节点的空右指针临时建立「线索」指向后继节点，访问完后还原，从而不需要任何栈。

```cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        TreeNode* cur = root;

        while (cur) {
            if (!cur->left) {
                // 无左子树：直接访问当前节点，转向右
                res.push_back(cur->val);
                cur = cur->right;
            } else {
                // 找左子树的最右节点（当前节点的中序前驱）
                TreeNode* pre = cur->left;
                while (pre->right && pre->right != cur) pre = pre->right;

                if (!pre->right) {
                    // 第一次到达：建立线索，继续深入左子树
                    pre->right = cur;
                    cur = cur->left;
                } else {
                    // 线索已存在（第二次到达）：还原指针，访问当前节点，转向右
                    pre->right = nullptr;
                    res.push_back(cur->val);
                    cur = cur->right;
                }
            }
        }
        return res;
    }
};
```

- 时间复杂度：O(n)（每个节点最多被「找前驱」的循环访问常数次）
- 空间复杂度：**O(1)**，只用了两个指针

---

## 本地验证（可运行示例）

```cpp
#include <iostream>
#include <stack>
#include <vector>
using namespace std;

// ...（TreeNode 定义见上）

int main() {
    // 树:     1
    //          \
    //           2
    //          /
    //         3
    TreeNode* root = new TreeNode(1, nullptr, new TreeNode(2, new TreeNode(3), nullptr));

    Solution s;   // 任选一个实现
    vector<int> res = s.inorderTraversal(root);

    for (int x : res) cout << x << " ";  // 期望输出: 1 3 2
    cout << "\n";
    return 0;
}
```

编译运行（沿用本目录的刷题配置）：

```bash
cd leetcode/solutions
mkdir -p build
clang++ -std=c++20 -O2 -g -Wall -Wextra -fsanitize=address,undefined <file>.cpp -o build/<file> && ./build/<file>
```
