class papa {
    int q;
    int r;
    int p;
}
class Debug {
    int main() {
        int [] a = new int[10];
        a[4] = 12;
        papa x = new papa();
        papa y = new papa();
        x.p = 5;
        y.p = 10;
        int b = x.p - y.p + a[4];
        println(b);
        return 0;
    }

}
