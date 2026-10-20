#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> merged(2 * n);
    for(int i = 0; i < 2 * n; i++) cin >> merged[i];
    sort(merged.begin(), merged.end());

    int mid = (2 * n - 1) / 2;
    cout << merged[mid] << '\n';
    
    return 0;
}