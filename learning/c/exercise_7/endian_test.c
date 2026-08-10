#include <stdio.h>

int main()
{
	union 
	{
		int data;
		char c;
	} test_data = { .data = 0x12345678 };

//	test_data.data = 0x12345678;

	printf("The data is 0x%x\n", test_data.data);
	printf("The charater is 0x%x\n", test_data.c);

	if(0x78 == test_data.c)
	{
		printf("little endian system\n");
	}

	return 0;

}
