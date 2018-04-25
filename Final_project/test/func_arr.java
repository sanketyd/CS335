class Debug {
    int print_arr(int [] a, int c, int b) {
        for (int i = 0; i < c; i++) {
            a[i] = i;
        }
        return b;
    }
    int main() {
        //int a = 20;
        int [] a = new int[10];
        int x = print_arr(a, 10, 3);
        for (int i = 0; i < 10; i++)
            println(a[i]);
    }
}
