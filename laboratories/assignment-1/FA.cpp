#include<string>
#include<unordered_map>
#include<vector>
#include<unordered_set>
#include<iostream>
#include<fstream>

class DFA{
private:
    std::unordered_map<int, std::unordered_map<char, int>> delta;
    int state;
    int end_state;
    std::unordered_set<char> alphabet;
public: 
    DFA(std::string pattern){
        this->state = 0;
        this->end_state = pattern.size();
        for(char c: pattern){
            alphabet.emplace(c);
        }
        
    }
    void parse_letter(char letter){
        state = delta[state][letter]; 
    }

    bool is_in_accepting_state(){
        return state==end_state;
    }
};


int main(int argc, char * argv[]){
    if(argc < 2){
        return;
    }
    std::string pattern = argv[0];
    std::string filename = argv[1];
    std::ifstream file; 
    file.open(filename);
    DFA dfa = DFA(pattern);
    int index = -1;
    while(file){
        char c = file.get();
        index++;

        dfa.parse_letter(c);
        if(dfa.is_in_accepting_state()){
            std::cout << "Znaleziono wzorzec: index: " << index-pattern.size() << std::endl;
        }
    }
    file.close();
}