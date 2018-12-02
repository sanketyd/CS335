public class dangling {
	public static void main(String[] args) {
		int i = 0;
		int[] a = {1, 2, 3};
		if(i <= 3) {
			a[i]++;
		}
		if(i >= 2) {
			a[i]--;
		} else {
			a[i] = 1;
		}
	}
}