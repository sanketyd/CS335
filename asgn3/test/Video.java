import java.util.*;
public abstract class Video {
	double Play_Duraton;
	Date Release_Date;
	Video(double Play_Duration,Date Release_Date){
		this.Play_Duraton = Play_Duration;
		this.Release_Date = Release_Date ;
	}
	double getDuration(){
		return this.Play_Duraton;
	}
	void setDuration(double duration){
		this.Play_Duraton = duration;
	}
	abstract Date getDate();
	abstract void setDate(Date date);
	
}
