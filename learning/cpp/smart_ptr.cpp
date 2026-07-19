#include <iostream>
#include <memory>

class TestClass {
public:
    TestClass() { std::cout << "Constructor called\n"; }
    ~TestClass() { std::cout << "Destructor called\n"; }
};

int main() {
    // 1. unique_ptr: 独占所有权，轻量级，无控制块
    std::unique_ptr<TestClass> uptr = std::make_unique<TestClass>();
    // uptr2 = uptr; // 编译错误！禁止拷贝
    std::unique_ptr<TestClass> uptr2 = std::move(uptr); // 只能移动所有权
    std::cout << "uptr is now: " << (uptr ? "valid" : "null") << "\n"; // 输出 null
    std::cout << "uptr2 is now: " << (uptr2 ? "valid" : "null") << "\n"; // 输出 null

    // 2. shared_ptr: 共享所有权，有控制块（强/弱引用计数）
    std::shared_ptr<TestClass> sptr1 = std::make_shared<TestClass>();
    {
        std::shared_ptr<TestClass> sptr2 = sptr1; // 引用计数 +1
        std::cout << "Use count: " << sptr1.use_count() << "\n"; // 输出 2
    } // sptr2 离开作用域，引用计数 -1
    std::cout << "Use count: " << sptr1.use_count() << "\n"; // 输出 1
    
    return 0;
} // sptr1 离开作用域，引用计数归零，对象被销毁
