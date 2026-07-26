package main

import (
	"fmt"
	"runtime"

	"github.com/fatih/color" // 引入刚才下载的第三方包
)

func main() {
	// 打印系统信息（普通白色）
	fmt.Printf("Hello from Go! Running on %s/%s\n", runtime.GOOS, runtime.GOARCH)

	// 使用第三方包打印彩色文字
	color.Red("This is a red message!")
	color.Green("Dependencies are working perfectly!")
	color.Yellow("You just imported a third-party package!")
}
