#include<iostream>
#include<vector>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin>>n>>m;

    vector<int> a(n);
    for(int i = 0; i < n; i++) cin>>a[i];

    while(m--){
        int q;
        cin>>q;

        int left = 0, right = n - 1;
        int ans = -1; 
        while(left <= right){
            int mid = left + (right - left) / 2;
            if(a[mid] >= q){
                ans = mid;
                right = mid - 1;
            }else left = mid + 1;
        }
        if(ans != -1 && a[ans] == q) cout << ans + 1 << ' ';
        else cout << -1 << ' ';
    }
    return 0;
}