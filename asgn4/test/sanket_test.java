class Main{
    int sum(int a, int b){
        if(a==b) return a*2;
        else return a+b;
    }
    void main(){
        int a = 3;
        int b = 2;
        int c = 99;
        switch(a) {
            case 1:
                if(b == 0) System.out.println(c);
            case 2:
                if(b==1) a = 10;
            case 3:
                if(b==2){
                    int x = 10;
                    while(x>1){
                        System.out.println(x);
                        x--;
                        for(int a = 0; a < 5; a++){
                            int l = add(x,a);
                            System.out.println(a);
                        }
                        System.out.println(a);
                    }
                    a = x*a;
                }
            default:
                a--;
                break;
        }
        System.out.println(a);
    }
}
