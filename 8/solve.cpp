#include <fstream>
#include <istream>
#include <iterator>
#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <optional>
#include <algorithm>
#include <map>
#include <functional>

struct Execution
{
    struct Instr
    {
        enum Op { ACC, JMP, NOP } op;
        int operand;
        
        inline static std::map<std::string, Op> opMap = { { "acc", ACC }, { "jmp", JMP }, { "nop", NOP } };
            
        friend std::istream &operator>>(std::istream &istream, Instr::Op &op) { std::string opStr; istream >> opStr; op = opMap[opStr]; return istream; }
        friend std::istream &operator>>(std::istream &istream, Instr &instr) { return istream >> instr.op >> instr.operand; }
    };

    const std::vector<Instr> instructions;
    std::vector<int> visited;
    int acc = 0, pc = 0;

    Execution(std::istream &input)
        : instructions(std::istream_iterator<Instr>(input), std::istream_iterator<Instr>()),
          visited(instructions.size(), false)
    {
    }

    void reset()
    {
        pc = acc = 0;
        for (auto &v : visited) v = false;
    }

    void execute(const Instr &instr)
    {
        visited[pc] = true;
        switch (instr.op)
        {
            case Instr::ACC: acc += instr.operand; pc++; break;
            case Instr::JMP: pc += instr.operand; break;
            case Instr::NOP: pc++; break;
        }
    }

    auto test(int replace)
    {
        auto replacedInstr = instructions[replace];
        switch (replacedInstr.op)
        {
            case Instr::NOP: replacedInstr.op = Instr::JMP; break;
            case Instr::JMP: replacedInstr.op = Instr::NOP; break;
            case Instr::ACC: return false;
        }

        while (true)
        {
            auto &instr = pc == replace ? replacedInstr : instructions[pc];
            if (pc == instructions.size()) return true; // successful execution
            else if (visited[pc]) return false;         // infinite loop
            else execute(instr);
        }
    }

    auto p1() { while (visited[pc] == false) execute(instructions[pc]); }
    auto p2() { for (auto x = 0; x < instructions.size() && !(reset(), test(x)); ++x); }
};

int main()
{
    auto ifstream = std::ifstream("input.txt");
    Execution e(ifstream);
    
    std::cout << (e.p1(), e.acc) << "\n"
              << (e.p2(), e.acc) << "\n"; 
}