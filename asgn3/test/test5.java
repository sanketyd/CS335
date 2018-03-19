class A {
    void printarray(int[] arr, int L) {
        int i;
        for (i = 0; i < L; i++) {
            int x = (arr[i] == 0) ? 10 : 20;
            System.out.println(x);
        }
    }
    static void main(String[] args) {
        int[] arr = new int[30];
        int i;
        for (i = 0; i < 30; i++) {
            arr[i] = (i % 2 == 0) ? 0 : 1;
        }
        printarray(arr, L);
    }
}
