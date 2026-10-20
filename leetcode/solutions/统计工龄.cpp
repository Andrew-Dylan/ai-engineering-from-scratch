#include<iostream>
#include<vector>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> cnt(51, 0);
    for(int i = 0; i < n; i++){
        int age;
        cin >> age;
        cnt[age]++;
    }
    
    for(int i = 0; i <= 50; i++){
        if(cnt[i] > 0){
            cout << i << ':' << cnt[i] << '\n';
        }
    }
    return 0;
}