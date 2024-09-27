#include <iostream>
#include <unistd.h>

int main (){
    int time = 0;

    while(1){
        time++;
        sleep(1);
        std::cout << "contagem: " << time << std::endl;
    }
    return 0;
}