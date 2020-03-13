#include <iostream>
#include <string> 
#include <math.h>

#define endl "\n"

using namespace std;

int  main(){

    int iterations=0;
    char ch;
    string line;
    string clean;
    double x;
    int y;
    bool pal;
    cin>>iterations;

    cin.get(ch);

    for(int i=0;i<iterations;i++){
        getline(cin,line);
        clean = "";
        for(int j=0;j<line.size();j++){
            if(line[j]<97 || line[j]>127)
                continue;
            clean += line[j];
        }
        cout<<clean.size()<<endl;
        x = sqrt(clean.size());
        y = x;

        if(y==x){
            cout<<x<<" "<<y<<"It's MAGICK"<<endl;
            cout <<clean<<endl;
            int count = 0;
            while(clean[count] == clean[countend]){                
                cout << clean[count] << " " << clean[countend] <<endl;
               count++;
               countend--;
               if(count == clean.size()-1){
                  pal = true;
               }

            }
            cout << pal <<endl;
           /* for(int i = 0; i < clean.size()/2; i++){
                if(clean[i] == clean[clean.size()]){
                    bool
                }
            }*/
        }
        
        
        
    }

    return 0;
}