class Main{
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
                            System.out.println(a);
                        }
                        System.out.prinln(a);
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
