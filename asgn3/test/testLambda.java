lambda inter{
    void usingLambda();
}
public class testLambda{
    public static void main(String[] args){
        inter r = () -> System.out.println("Yo");
        r.usingLambda();
    }
}
