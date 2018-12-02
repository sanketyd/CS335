public class loop {
	public static void main(String[] args) {
		int i,j,k, res;
		for(res = 0, i = 0; i < 10; i++) {
			for( j = 0; j < 10; j++) {
				for( k = 0; k < 10; k++) {
					res += 1;
				}
			}
		}

		System.out.println("res = " + res);
	}
}