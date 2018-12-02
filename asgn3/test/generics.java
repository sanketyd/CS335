class Generic {
    static <?T?> genericDisplay(T element) {
        System.out.println(element);
        return element;
    }
    static void main(String[] args) {
        genericDisplay(11);
    }
}
