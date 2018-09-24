#include <iostream>

extern "C"
{
void foo()
{
   std::cout << "fooish" << std::endl;
}
}

void bar()
{
   std::cout << "barish" << std::endl;
}

int main()
{
   foo();
   bar();
}
