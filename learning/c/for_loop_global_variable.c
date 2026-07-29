#include <stdio.h>
long g_sum = 0;
void test_for_loop(int number) {
	long sum=0;
	for(int i=0; i<number; i++) {
		g_sum+=i;
	}
}

void main() {
	int number=100;
	test_for_loop(number);
	printf("The sum of %d numbers is %ld\n", number, g_sum);
}
