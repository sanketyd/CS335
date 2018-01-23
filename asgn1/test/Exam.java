import java.lang.reflect.Field;

public class Exam extends ExamCentres{
	private String Title;
	private int CentreCode;
	public Exam(String Title, int Centre_Code){
		this.Title = Title;
		this.CentreCode = Centre_Code;
	}
	String getTitle(){
		return this.Title;
	}
	void setTitle(String title){
		this.Title = title;
	}
	int getCode(){
		return this.CentreCode;
	}
	void setCode(int code){
		this.CentreCode = code;
	}
	void printCentreName(){
		Class<ExamCentres> c = ExamCentres.class;
		Field[] fields = this.getClass().getSuperclass().getDeclaredFields();
		for(int i=0;i < fields.length;i++ ){
			
			try {

				Object code = fields[i].get(c);
				if(code.equals(this.CentreCode) == true){
					System.out.println(fields[i]);
					return;
				}

		      } catch ( 
		             SecurityException | IllegalAccessException ex) {
		      System.out.println(ex.getMessage());
		      }
		}
		System.out.println("Unknown");
		/*switch(this.CentreCode){
		case 10:System.out.println("LKO");break;
		case 20:System.out.println("CNB");break;
		case 30:System.out.println("AGC");break;
		case 40:System.out.println("ALD");break;
		case 50:System.out.println("VNS");break;
		default: System.out.println("Unknown");
		}*/
	}
	boolean isValidCentre(){
		Class<ExamCentres> c = ExamCentres.class;
		Field[] fields = this.getClass().getSuperclass().getDeclaredFields();
		for(int i=0;i < fields.length;i++ ){
			
			try {

				Object code = fields[i].get(c);
				if(code.equals(this.CentreCode) == true){
					return true;
				}

		      } catch ( 
		             SecurityException | IllegalAccessException ex) {
		      System.out.println(ex.getMessage());
		      }
		}
		return false;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Exam exam = new Exam("Phy",20);
		Exam exam2 = new Exam("Chem",30);
		exam2.printCentreName();
		boolean check = exam.isValidCentre();
		System.out.println(check);
	}
}


