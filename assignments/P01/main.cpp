#include "poker_game.hpp"
#include <iomanip>

int main(){

    Term::IO io;
    Game k;
    Deck D(52);
    Hand player1(26);
    Hand player2(26);
    bool cont = true;
    for(int i=0;i<50;i++){
        D.Shuffle();
        //D.Print(2,true);
        break;
        io << Term::sleep(200); 
    }

   D.Split(player1, player2);
   player1.Shuffle();
  // player1.Print(4, true);
   
 
   player2.Shuffle();
  // player2.Print(4, true); 
while(cont){
  io << "Cards: " << player1.Size() << "     Cards: " << player2.Size() <<"\n";
   CardContainer i(player1.Play(), player2.Play());
    
   i.Print(2, false);
    io<<"Player 1        Player 2\n";

    k.Distribute(k.Compare(i.Get(0), i.Get(1)), player1, player2, i);
     
    if(player1.Size() == 0 || player2.Size() == 0){
     cont = k.End(player1.Size(), player2.Size());
    }

}
    return 0;
}