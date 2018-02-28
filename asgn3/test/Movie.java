import java.util.*;
public class Movie extends Video implements Comparable<Movie>{
	String Movie_Name;
	public enum rating {A, U, UA }
	rating Rating;
	public Movie(double Play_Duration, Date Release_Date,String name,rating Rating) {
		super(Play_Duration, Release_Date);
		this.Movie_Name = name;
		this.Rating = Rating;
	}
	Date getDate(){
		return this.Release_Date;
	}
	void setDate(Date date){
		this.Release_Date = date; 
	}
	public int compareTo(Movie movie){
        int DateCmp = Release_Date.compareTo(movie.Release_Date);
        int NameCmp = Movie_Name.compareTo(movie.Movie_Name);
        if(DateCmp == 0 && NameCmp == 0){
        	return 0;
        }
        if(NameCmp > 0){
        	return 1;
        }
        if(NameCmp < 0){
        	return -1;
        }
        if(DateCmp > 0){
        	return 1;
        }
        else return -1;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Date date = new Date();
		Movie movie2 = new Movie(23.5,date,"Movie2",rating.U);
		Movie movie = new Movie(20.5,date,"Random Movie",rating.A);
		System.out.println(movie.compareTo(movie2));
	}
	
}
