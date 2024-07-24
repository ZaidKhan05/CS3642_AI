#include <cstring>
#include <iostream>
#include <cstdlib>	// Provides EXIT_SUCCESS, NULL, rand, size_t
#include <ctime>	// to get a good seed for rand()

// compile with g++ gendata.cpp
// works for version 9.4.0:
// g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0

// generate 4-pixel data points with ground truth for bright or dim (more than one illuminated pixel)
// accepts two arguments, one for number of datapoints to generate
// second "test" will add ground truth values of dim/bright as last csv value
// replace with -1/1 if needed
int main( int argc, char** argv)
{
   time_t t0;
   clock_t c0;
   srand( time( &t0));
   srand( clock());
   int roll = rand()%2;

   bool test = false;
   int datapoints = 100;

   if ( argc == 3) {
      datapoints = atoi( argv[1]);
      if( strncmp( argv[2], "test", 4) == 0) {
         test = true;
      }
   } else if ( argc == 2) {
      datapoints = atoi( argv[1]);
   } else {
      printf("Usage: %s <number of data points> <test | train>\n", argv[0]);
      return(-1);
   }

   int sum = 0;
   for( int i = 0; i < datapoints*4; ++i) {
      roll = rand()%2;
      sum+= roll;
      if( i%4 == 3) {
         printf("%d", roll);
      } else {
         printf("%d, ", roll);
      }
      if( !test && (i%4 == 3)) {
         if ( sum > 1) {
            printf(", bright\n");
         } else {
            printf(", dim\n");
         }
         sum = 0;
      } else if ( test & (i%4 == 3)) {
         printf("\n");
      } else {
         ;        // do nothing, this list selection can really be optimized
      }
   }
   return(0);
}

