#include<iostream>
#include<vector>
using namespace std;


class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> res;
        if(matrix.empty()) return res;
        int m = matrix.size(), n = matrix[0].size();
        int left = 0, right = n - 1, top = 0, bottom = m - 1;
        while(left <= right && top <= bottom){
            for(int j = left; j <= right; j++){
                res.push_back(matrix[top][j]);
            }
            top++;
            for(int i = top; i <= bottom; i++){
                res.push_back(matrix[i][right]);
            }
            right--;
            if(top <= bottom){
                for(int j = right; j >= left; j--){
                    res.push_back(matrix[bottom][j]);
                }
                bottom--;
            }
        }
        return res;
    }
};

int main(){
    Solution s;
    struct Case{
        vector<vector<int>> input;
        vector<int> expected;
    };
    vector<Case> cases = {
        {{{1,2,3},{4,5,6},{7,8,9}}, {1,2,3,6,9,8,7,4,5}},
        {{{1,2,3,4},{5,6,7,8},{9,10,11,12}}, {1,2,3,4,8,12,11,10,9,5,6,7}},
        {{{1}}, {1}},
        {{{1},{2},{3}}, {1,2,3}},
        {{{1}}, {1}},
    };
}