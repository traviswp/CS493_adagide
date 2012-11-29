#include <iostream>
using namespace std;
int main(){
while(1)
{
cout<<"Enter some text, friend:";
string input;
getline(cin, input, '\n');
cout<<"you entered:\n" << input << "\n";
//cout<<"hello world!\n";
}
return 0;
}