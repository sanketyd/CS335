class T{
	public T(){

	}
	void f(){
		a = 'a';
		b = 47114711;
		c = 'c';
		d = 1234;
		e = 3.141592897932;
		f = '*';
		name = "abc";
	}
	char a;
	int b;
	char c;
	short d;
	double e;
	String name = new String();
	char f;
}

public class struct_func{
	public static void main(String[] args){
		T k = new T();
		k.f();
	}
}