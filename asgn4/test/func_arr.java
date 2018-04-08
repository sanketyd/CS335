class Debug {
    int add(int a, int b) {
        return a + b;
    }
    int main() {
        //int a = 20;
        int a = 19;
        int [][] b = new int[a][20];
        b[2][3] = 10;
	b[1][2] = 20;
	int c = add(b[2][3],b[1][2]);
    }
}
