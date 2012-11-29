#include <iostream>
using namespace std;
int main(int argc, char** args){
while(1)
{
for(int i=0; i<argc; i++)
{
	cout << args[i] << '\n';
}
cout<<"Enter some text, friend:";
string input;
getline(cin, input, '\n');
cout<<"you entered:\n" << input << "\n";
//cout<<"hello world!\n";
}
return 0;
}