class papa {
    int q;
    int r;
    int add(int a, int b) {
        this.r = 100;
        a = this.r;
        return a + this.r;
    }
}

class Debug {
    int sub(int a, int b) {
        return a - b;
    }
    int main() {
        int j = sub(10, 4);
        println(j);
        papa x = new papa();
        println(x.q);
        int q = x.add(10, 40);
        println(q);
        papa y = new papa();
        y.r = 30;
        int c = 23 + y.r;
        println(c);
        return 0;
    }

}
