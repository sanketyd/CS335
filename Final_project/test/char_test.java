class char_test{
    int main(){
        int size;
        input(size);
        char []a = new char[size];
        for(int i = 0; i < size; i++){
            a[i] = 'a' + i;
        }
        for(int i = 0; i < size; i++){
            println(a[i]);
            println(' ');
        }
        return 0;
    }
}
