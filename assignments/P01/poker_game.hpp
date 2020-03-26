#include "termio.h"
#include "playingcard.hpp"
#include <algorithm> // std::random_shuffle
#include <iostream>
#include <string>
#include <deque>
#include <random>
#include <time.h>
#include <stdlib.h>

using namespace std;
Term::IO io;
const string spade = "♠";
const string diamond = "♦";
const string heart = "♥";
const string club = "♣";

const string suits[4] = {"♠", "♦", "♣", "♥"};

// Black background        blue ,  red , blue , red
const string colors2[4] = {"&60", "&20", "&60", "&20"};

// Colored background      blue  , red  , blue , red
const string colors[4] = {"&16", "&12", "&16", "&12"};

// Card labels (could be "Iron Man" or "Charmander" or "Elf" ... anything)
const string ranks[13] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};


/*
  ██████╗ █████╗ ██████╗ ██████╗  ██████╗ ██████╗ ███╗   ██╗████████╗ █████╗ ██╗███╗   ██╗███████╗██████╗
 ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝██╔══██╗
 ██║     ███████║██████╔╝██║  ██║██║     ██║   ██║██╔██╗ ██║   ██║   ███████║██║██╔██╗ ██║█████╗  ██████╔╝
 ██║     ██╔══██║██╔══██╗██║  ██║██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██║██║██║╚██╗██║██╔══╝  ██╔══██╗
 ╚██████╗██║  ██║██║  ██║██████╔╝╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║██║ ╚████║███████╗██║  ██║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
*/

class CardContainer {
protected:
    Term::IO io;
    deque<Card *> Cards;
    int RandomIndex();
    struct CardCompare {
        bool operator()(Card *l, Card *r) {
            return *l < *r;
        }
    };

public:
    int contSize;
    CardContainer(int);
    CardContainer(Card* a, Card* b);
    void Add(Card *);
    bool isEmpty();
    void Order();
    Card *Remove();
    void Reset();
    void Shuffle();
    int Size();
    void Print(int columns, bool clear);
    Card* Get(int i);
    bool Compare(Card* a, Card* b);
};
bool CardContainer::Compare(Card* a, Card* b){
  CardCompare g;
  return g(a, b);
}

CardContainer::CardContainer(int numCards) {
    for (int i = 0; i < numCards; i++) {
        Cards.push_back(new Card(i));
    }
}
CardContainer::CardContainer(Card* a, Card* b){
 // Cards.resize(2);
  Cards.push_back(a);
  Cards.push_back(b);
 // contSize = 2;
}
void CardContainer::Add(Card *card) {
    // check if card already in container?
    // allow go over 52 ??
    //contSize++;
   // Cards.resize(contSize);
    Cards.push_back(card);
 // currentCount = Cards.size();
}

bool CardContainer::isEmpty() {
    return Cards.empty();
}

void CardContainer::Order() {
    sort(Cards.begin(), Cards.end(), CardCompare());
}

Card *CardContainer::Remove() {
    Card *temp = Cards.front();
   // contSize--;
   // Cards.resize(contSize);
    Cards.pop_front();
    return temp;
}

void CardContainer::Reset() {
    for (int i = 0; i < Cards.size() - 1; i++) {
        delete Cards[i];
        Cards[i] = new Card(i);
    }
}

void CardContainer::Shuffle() {
  srand(time(0));
    for (int i = 0; i < Cards.size() - 1; i++) {
        int j = i + rand() % (Cards.size() - i);
        swap(Cards[i], Cards[j]);
    }
}

int CardContainer::Size() {
    return Cards.size();
}

void CardContainer::Print(int columns = 1, bool clear = false) {
    int i = 0;
    deque<string> cards;

    if (clear) {
        io << Term::clear;
    }

    for (auto c : Cards) {
        cards.push_back(c->Repr());

        i++;
        if (i == columns) {
            io << Term::fuse(cards) << "\n";
            i = 0;
            cards.clear();
        }
    }

    // any cards left in the deque should be
    // printed out.
    if (cards.size() > 0) {
        io << Term::fuse(cards) << "\n";
    }
}
Card* CardContainer::Get(int i){
      Card *temp = Cards[i];
      return temp;
}
/*
 ██╗  ██╗ █████╗ ███╗   ██╗██████╗
 ██║  ██║██╔══██╗████╗  ██║██╔══██╗
 ███████║███████║██╔██╗ ██║██║  ██║
 ██╔══██║██╔══██║██║╚██╗██║██║  ██║
 ██║  ██║██║  ██║██║ ╚████║██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝
*/

class Hand : public CardContainer{
protected:
int handSize;

public:
    Hand(int);
    void Print(int columns, bool clear);
    Card* Play();
    void PushCards(CardContainer temp);
    void PushCard(Card* a);
    void Shuffle();
    int Size();
    void Remove();
};

void Hand::Shuffle(){
srand(time(0));
  for (int i = 0; i < Cards.size() - 1; i++) {
        int j = i + rand() % (Cards.size() - i);
        swap(Cards[i], Cards[j]);
    }
}
//Hand::Hand() : CardContainer(26){};
void Hand::PushCard(Card* a){
  handSize++;
  //Cards.resize(handSize);
  Cards.push_back(a);
}
Hand::Hand(int size) : CardContainer(size) {
    handSize = size;
}
void Hand::Print(int columns = 1, bool clear = false) {
    int i = 0;
    deque<string> cards;

    if (clear) {
        io << Term::clear;
    }

    for (auto c : Cards) {
        cards.push_back(c->Repr());

        i++;
        if (i == columns) {
            io << Term::fuse(cards) << "\n";
            i = 0;
            cards.clear();
        }
    }

    // any cards left in the deque should be
    // printed out.
    if (cards.size() > 0) {
        io << Term::fuse(cards) << "\n";
    }
}
Card* Hand::Play(){
    Card *temp = Cards.front();
    handSize--;
    Cards.pop_front(); 
    //Cards.resize(handSize);
    return temp;

}
void Hand::PushCards(CardContainer temp){
  for (int i = 0; i < Cards.size() - 1; i++) {
    this->Cards.push_back(Cards.front());
    Cards.pop_front();
  }
  handSize++;
}
void Hand::Remove(){
      Card *temp = Cards.front();
    Cards.pop_front();
    handSize--;
}
int Hand::Size(){
  return handSize;
}
/*
 ██████╗ ███████╗ ██████╗██╗  ██╗
 ██╔══██╗██╔════╝██╔════╝██║ ██╔╝
 ██║  ██║█████╗  ██║     █████╔╝
 ██║  ██║██╔══╝  ██║     ██╔═██╗
 ██████╔╝███████╗╚██████╗██║  ██╗
 ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝
*/

class Deck : public CardContainer {
protected:
    int deckSize;

public:
    Deck(int);
    Card *Draw();
    void Print(int, bool);
    void Split(Hand a, Hand b);
    friend Hand;
};

Deck::Deck(int size) : CardContainer(size) {
    deckSize = size;
}

Card *Deck::Draw() {
    Card *temp = Cards.back();
    Cards.pop_back();
    return temp;
}

void Deck::Print(int columns = 1, bool clear = false) {
    int i = 0;
    deque<string> cards;

    if (clear) {
        io << Term::clear;
    }

    for (auto c : Cards) {
        cards.push_back(c->Repr());

        i++;
        if (i == columns) {
            io << Term::fuse(cards) << "\n";
            i = 0;
            cards.clear();
        }
    }

    // any cards left in the deque should be
    // printed out.
    if (cards.size() > 0) {
        io << Term::fuse(cards) << "\n";
    }
}
void Deck::Split(Hand a, Hand b){
  Shuffle();
  Shuffle();
  Shuffle();
  Shuffle();
  for (int i = 0; i < 26; i++) {
      //int j = i + rand() % (Cards.size() - i);
      a.PushCard(Draw());
      //a.Shuffle();
      b.PushCard(Draw());
     // b.Shuffle();
  }

}


/*
  ██████╗  █████╗ ███╗   ███╗███████╗
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
 ██║  ███╗███████║██╔████╔██║█████╗
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
*/

class Game {
protected:
public:
  int Compare(Card* a, Card* b);
  bool End(int p1Size, int p2Size);
  void War(Hand& a, Hand& b, CardContainer& x);
  void Distribute(int i, Hand& a, Hand& b, CardContainer& x);
};

void Game::War(Hand& a, Hand& b, CardContainer& x){
    CardContainer j(a.Play(), b.Play());
   if(a.Size() < 3 || b.Size() < 3){
     for(int i = 0; i < 3; i++){
      j.Add(a.Play());
      j.Add(b.Play());
    }
   }else{
      for(int i = 0; i < a.Size(); i++){
          j.Add(a.Play());
      }
      for(int i = 0; i < b.Size(); i++){
          j.Add(b.Play());
      }
   }
    
    j.Add(x.Remove());
    j.Add(x.Remove());

    Compare(j.Get(0), j.Get(1));

}

void Game::Distribute(int i, Hand& a, Hand& b, CardContainer& x){
 // io<< x.isEmpty() << " " << x.Size() <<"\n";
  switch(i){
     case 1:{
         for (int i = 0; i < x.Size()+1; i++) {
           io<<"P1 gets it\n\n";
           a.PushCard(x.Remove());
          }
          io<< x.isEmpty() <<"\n";
        break;
       }
      case 2:{
          for (int i = 0; i < x.Size()+1; i++) {
            io<<"P2 gets it\n\n";
             b.PushCard(x.Remove());
          }
          io<< x.isEmpty() << " " << x.Size() <<"\n";
        break;
       }
      case 0:{
        War(a, b, x);
        break;
      }  
  }
}
int Game::Compare(Card* a, Card* b){

  if(*a > *b){
  //  io<<"P1 gets it\n\n";
    return 1;
  }else if(*a < *b){
   // io<<"P2 gets it\n\n";
    return 2;
  }else{
    io<<"WAR\n\n";
    return 0;
  }
}




bool Game::End(int p1Size, int p2Size){
 io<<" _____ _____ _____ _____    _____ _____ _____ _____ \n"
   <<"|   __|  _  |     |   __|  |     |  |  |   __| __  |\n"
   <<"|  |  |     | | | |   __|  |  |  |  |  |   __|    -|\n"
   <<"|_____|__|__|_|_|_|_____|  |_____|-___/|_____|__|__|\n";
 
 if(p2Size == 0){
     io << " _____ __    _____ __ __ _____ _____    ___      _ _ _ _____ _____ _____ \n"
        <<"|  _  |  |  |  _  |  |  |   __| __  |  |_  |    | | | |     |   | |   __|\n"
        <<"|   __|  |__|     |_   _|   __|    -|   _| |_   | | | |-   -| | | |__   |\n"
        <<"|__|  |_____|__|__| |_| |_____|__|__|  |_____|  |_____|_____|_|___|_____|\n";
 }else{
   io <<" _____ __    _____ __ __ _____ _____    ___    _ _ _ _____ _____ _____ \n"
      <<"|  _  |  |  |  _  |  |  |   __| __  |  |_  |  | | | |     |   | |   __|\n"
      <<"|   __|  |__|     |_   _|   __|    -|  |  _|  | | | |-   -| | | |__   |\n"
      <<"|__|  |_____|__|__| |_| |_____|__|__|  |___|  |_____|_____|_|___|_____|\n";
 }

   return false;                                                                     
}
