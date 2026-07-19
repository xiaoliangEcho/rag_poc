#include <iostream>
#include <memory>

// Base 对象内存布局：
// ┌─────────────┐
// │   vptr      │ ← 指向 Base 类的 vtable
// ├─────────────┤
// │   base_data  │
// └─────────────┘

// Derived 对象内存布局：
// ┌─────────────┐
// │   vptr      │ ← 指向 Derived 类的 vtable（覆盖了 Base 的 vtable）
// ├─────────────┤
// │   base_data  │
// ├─────────────┤
// │  derived_data│
// └─────────────┘

// 编译时：编译器知道 b 是 Base* 类型，所以生成通过 vptr 调用的代码

// 运行时：b 实际指向 Derived 对象，所以 b->vptr 指向 Derived 的 vtable

// 结果：调用 Derived::show，实现动态绑定


// 类型	           声明方式	               是否必须重写	            是否可实例化
// 普通虚函数	virtual void func()	       ❌ 不必	                ✅ 可以
// 纯虚函数	    virtual void func() = 0	   ✅ 必须	               ❌ 不可以（抽象类）


class Base {
public:
    virtual void show() { std::cout << "Base show\n"; }
    virtual void test() { std::cout << "Base::test\n"; }
    int base_data;
};

class Derived : public Base {
public:
    void show() override { std::cout << "Derived show\n"; }
    int derived_data;
};

int main() {
    //Base* b = new Derived();
    
    
    // 底层原理：b 指向的对象内存最前面有一个隐藏的 vptr 指针
    // vptr 指向 Derived 类的 vtable，vtable 中存储了 Derived::show 的地址
    // 程序通过 vptr 查表，实现了动态绑定
    std::cout << "Base object size: " << sizeof(Base) << "\n";
    std::cout << "Derived object size: " << sizeof(Derived) << "\n";
    // 输出通常为 8 或 16（取决于指针大小 + 成员变量）
    
    // ❌ 不要 delete bp！
    // 函数结束时会自动调用 d 的析构函数
    // Derived d; //d 在栈上分配
    // Base* bp = &d; //bp 指向栈上的对象

    // unique_ptr - 独占所有权
    std::unique_ptr<Base> bp = std::make_unique<Derived>();
    // 或 std::unique_ptr<Base> bp(new Derived());

    
    // 在堆上分配
    //Base* bp = new Derived();  // ✅ 正确

    bp->show(); // Derived::show（动态绑定）
    bp->test();  // Base::test（从 Derived 的 vtable 中找 Base::test）

    //在堆上分配的需要手动delete
    // delete bp;
    return 0;
}
