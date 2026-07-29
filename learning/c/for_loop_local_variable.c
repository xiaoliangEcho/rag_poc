#include <stdio.h>

long test_for_loop(int number) {
	long sum=0;
	for(int i=0; i<number; i++) {
		sum+=i;
	}
	return sum;
}

void main() {
	int number=100;
	long sum;
	sum = test_for_loop(number);
	printf("The sum of %d numbers is %ld\n", number, sum);
}
