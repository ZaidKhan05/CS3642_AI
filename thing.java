import java.util.Scanner;
class thing {
    public static String twosCompliment(String binary) {
        String twos = "";
        boolean addOne = true;
        String temp = "";
        //reverse the string
        for(int i = binary.length() - 1; i >= 0; i--) {
            temp += binary.charAt(i);
        }
        for (int i = 0; i < temp.length(); i++) {
            if(addOne) {
                if (temp.charAt(i) == '0') {
                    twos += '0';
                } else {
                    twos += '1';
                    addOne = false;
                }
            } else {
                if (temp.charAt(i) == '1') {
                    twos += '0';
                } else {
                    twos += '1';
                }
            }
            
        }
        //reverse the string again
        String temp2 = "";
        for(int j = twos.length() - 1; j >= 0; j--) {
            temp2 += twos.charAt(j);
        }
        
        twos = temp2;
        return twos;
    }
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        Scanner sc = new Scanner(System.in);
        System.out.println("give me a binary string to find the twos compliment of:");
        String binary = sc.nextLine();
        System.out.println("The twos compliment of " + binary + " is " + twosCompliment(binary));
    }
}